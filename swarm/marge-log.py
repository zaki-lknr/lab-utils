import json
import datetime

new_data_file = 'today.json'
stored_data_file = 'all-checkins.json'

# print(files)

def get_marge_data():
    all_checkins = []
    with open(stored_data_file) as f:
        all_checkins = json.load(f)

    with open(new_data_file) as f:
        d = json.load(f)
        checkins = d['response']['checkins']['items']

        index = 0
        for checkin in checkins:
            if checkin['id'] not in (i['id'] for i in all_checkins):
                all_checkins.insert(index, checkin)
                index += 1
                # fixme: 順序が逆になるのでtodayにallを足すようにする (か、ソート処理を組み込む)

    # for c in all_checkins:
    #     print(c['id'] + ', ' + str(datetime.datetime.fromtimestamp(c['createdAt'])) + ', ' + c['venue']['name'])
    #     z = datetime.datetime.fromtimestamp(c['createdAt'])
    #     zz = c['createdAt']

    # print(type(z))
    # print(zz)
    # print(str(z))
    # print(json.dumps(all_checkins, ensure_ascii=False))
    return(all_checkins)

def statistics(checkins):
    data = {
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

        if item:
            item['count'] += 1
            item['oldest'] = str(checkin_time)
            item['checkins'].append((checkin_time).strftime('%m/%d'))
        else:
            diff = current_dt - checkin_time
            data['statistics'][checkin_id] = {
                'count': 1,
                'name': checkin['venue']['name'],
                'latest': str(checkin_time),
                'passed': str(diff.days) + "d, " + str(int(diff.seconds / 60 / 60)) + "h",
                'oldest': str(checkin_time),
                'checkins': [(checkin_time).strftime('%m/%d')],
            }

    data['statistics'] = dict(sorted(data['statistics'].items(), key=lambda x: x[1]['count'], reverse=True))
    data['expired'] = list(expired_work)
    return(data)

if __name__ == "__main__":
    checkins = get_marge_data()
    data = statistics(checkins)
    # print(json.dumps(checkins, ensure_ascii=False))
    print(json.dumps(data, ensure_ascii=False))
