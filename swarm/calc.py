import json
import datetime
import argparse

stored_data_file = 'logs/all-checkins-current.json'
threshold_file = 'threshold.json'
statistics_file = 'logs/stat.json'
# print(files)

def statistics(src_file, thr_file):

    with open(src_file) as f:
        checkins = json.load(f)

    data = {
        'threshold': [],
        'lost': {},
        'interval': {},
        'statistics': {},
        'expired': [],
    }
    expired_work = set()
    current_dt = datetime.datetime.now()
    limit_sec = int((current_dt + datetime.timedelta(days=-30)).timestamp())

    # aggregate all checkin
    for checkin in checkins:
        checkin_id = checkin['venue']['id']
        checkin_time = datetime.datetime.fromtimestamp(checkin['createdAt'])
        item = data['statistics'].get(checkin_id)
        if (limit_sec > checkin['createdAt']):
            # expired item
            if (not item):
                expired_work.add(checkin['venue']['name'])
            continue

        diff = current_dt - checkin_time
        lost = int((checkin['createdAt'] - limit_sec) / 60 / 60 / 24)
        if item:
            # update item
            item['count'] += 1
            item['oldest'] = str(checkin_time)
            item['lost'] = lost
            item['checkins'].append((checkin_time).strftime('%m/%d'))
        else:
            # new item
            data['statistics'][checkin_id] = {
                'count': 1,
                'name': checkin['venue']['name'],
                'latest': str(checkin_time),
                'passed': int(diff.total_seconds() / 60 / 60 / 24),
                'oldest': str(checkin_time),
                'lost': lost,
                'checkins': [(checkin_time).strftime('%m/%d')],
            }

    data['statistics'] = dict(sorted(data['statistics'].items(), key=lambda x: x[1]['count'], reverse=True))
    data['expired'] = list(expired_work)

    with open(thr_file) as f:
        threshold = json.load(f)

    # 閾値定義ファイル順に検査
    for key, item in threshold.items():
        if (d := data['statistics'].get(key)):
            # print(d)
            # st = {
            #     'name': item['name'],
            #     'count': str(d['count']) + '/' + str(item['count']),
            #     'interval': str(int(d['passed'] / 24)) + '/' + str(item['threshold'])
            # }
            pass_h = d['passed']
            lost_h = d['lost']

            if pass_h >= item['threshold'] or d['count'] <= item['count']:
                st = 'c:{: >2}({: >2})/'.format(d['count'], item['count'])
                st += 'int:{: >2}({: >2})/'.format(pass_h, item['threshold'])
                st += 'exp:{: >2}'.format(lost_h)
                st += '| ' + item['name']
                # print(st)
                data['threshold'].append(st)

    # データサブセット
    stat = []
    for key, item in data['statistics'].items():
        lost = item['lost']
        passed = item['passed']
        name = "(" + str(item['count']) + "/" + "pass:" + str(passed) + "/" + "lost:" + str(lost) + ") " + item['name']
        stat.append({
            'count': item['count'],
            'name': name,
            'latest': item['latest'],
            'passed': passed,
            'oldest': item['oldest'],
            'lost': lost
        })


    # data['lost'] = sorted(stat, key=lambda x:x['lost'])

    lost_items = {}
    for item in stat:
        if (l := lost_items.get(item['lost'])):
            l.append(item['name'])
        else:
            lost_items[item['lost']] = [item['name']]
    data['lost'] = dict(sorted(lost_items.items(), key=lambda x:x[0]))

    interval_items = {}
    for item in stat:
        if (l := interval_items.get(item['passed'])):
            l.append(item['name'])
        else:
            interval_items[item['passed']] = [item['name']]
    data['interval'] = dict(sorted(interval_items.items(), key=lambda x:x[0], reverse=True))

    return(data)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--src", help="src file")
    p.add_argument("--out", help="output file")
    p.add_argument("--threshold", help="threshold configure file")
    args = p.parse_args()

    src_file = args.src or stored_data_file
    out_file = args.out or statistics_file
    thr_file = args.threshold or threshold_file

    data = statistics(src_file, thr_file)

    with open(out_file, mode='w') as f:
        f.write(json.dumps(data, ensure_ascii=False, indent=2))
