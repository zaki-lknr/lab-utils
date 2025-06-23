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

if __name__ == "__main__":
    checkins = get_marge_data()
    print(json.dumps(checkins, ensure_ascii=False))
