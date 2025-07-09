import json
import datetime

data_dir = 'logs/'
new_data_file = 'today.json'
stored_data_file = 'all-checkins.json'
new_stored_data_file = 'all-checkins-current.json'
statistics_file = 'stat.json'
# print(files)

def get_data():
    with open(data_dir + new_stored_data_file) as f:
        all_checkins = json.load(f)
    return all_checkins

def statistics(checkins):
    data = {
        'lost': {},
        'interval': {},
        'statistics': {},
        'expired': [],
    }
    expired_work = set()
    current_dt = datetime.datetime.now()
    limit_sec = int((current_dt + datetime.timedelta(days=-30)).timestamp())

    for checkin in checkins:
        checkin_id = checkin['venue']['id']
        checkin_time = datetime.datetime.fromtimestamp(checkin['createdAt'])
        item = data['statistics'].get(checkin_id)
        if (limit_sec > checkin['createdAt']):
            # 期限切れ
            if (not item):
                expired_work.add(checkin['venue']['name'])
            continue

        diff = current_dt - checkin_time
        lost = int((checkin['createdAt'] - limit_sec) / 60 / 60)
        if item:
            item['count'] += 1
            item['oldest'] = str(checkin_time)
            item['lost'] = lost
            item['checkins'].append((checkin_time).strftime('%m/%d'))
        else:
            data['statistics'][checkin_id] = {
                'count': 1,
                'name': checkin['venue']['name'],
                'latest': str(checkin_time),
                'passed': int(diff.total_seconds() / 60 / 60),
                'oldest': str(checkin_time),
                'lost': lost,
                'checkins': [(checkin_time).strftime('%m/%d')],
            }

    data['statistics'] = dict(sorted(data['statistics'].items(), key=lambda x: x[1]['count'], reverse=True))
    data['expired'] = list(expired_work)

    # データサブセット
    stat = []
    for item in data['statistics'].values():
        stat.append({
            'count': item['count'],
            'name': "(" + str(item['count']) + ") " + item['name'],
            'latest': item['latest'],
            'passed': int(item['passed'] / 24),
            'oldest': item['oldest'],
            'lost': int(item['lost'] / 24),
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
    checkins = get_data()
    data = statistics(checkins)

    # with open(data_dir + new_stored_data_file, mode='w') as f:
    #     f.write(json.dumps(checkins, ensure_ascii=False))

    # with open(data_dir + statistics_file, mode='w') as f:
    #     f.write(json.dumps(data, ensure_ascii=False))

    print(json.dumps(data, ensure_ascii=False, indent=2))
