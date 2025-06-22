import json

base_path = '/path/to/'
files = [
    base_path + 'log-2.json',
    base_path + 'log-1.json',
]

# print(files)

all_checkins = []

for file in files:
    # print(file)

    with open(file) as f:
        d = json.load(f)
        checkins = d['response']['checkins']['items']

        for checkin in checkins:
            if checkin['id'] not in (i['id'] for i in all_checkins):
                all_checkins.append(checkin)

# for c in all_checkins:
#     print(c['id'] + ', ' + c['venue']['name'])

print(json.dumps(all_checkins, ensure_ascii=False))
