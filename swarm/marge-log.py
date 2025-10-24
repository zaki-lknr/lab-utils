import json
import datetime
import argparse

new_data_file = 'logs/today.json'
stored_data_file = 'logs/all-checkins.json'
new_stored_data_file = 'logs/all-checkins-current.json'
# print(files)

def get_marge_data(base_file, add_file):
    all_checkins = []
    with open(base_file) as f:
        all_checkins = json.load(f)

    with open(add_file) as f:
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

    return(all_checkins)

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--base", help="base file")
    p.add_argument("--add", help="add file")
    p.add_argument("--out", help="output file")
    args = p.parse_args()

    base_file = args.base or stored_data_file
    add_file = args.add or new_data_file
    output_file = args.out or new_stored_data_file

    checkins = get_marge_data(base_file, add_file)
    with open(output_file, mode='w') as f:
        f.write(json.dumps(checkins, ensure_ascii=False))
