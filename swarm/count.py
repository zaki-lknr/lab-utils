import json
import datetime
import argparse

threshold_file = 'threshold.json'
statistics_file = 'logs/stat.json'

def statistics(stat_file, thr_file):

    with open(stat_file) as f:
        stats = json.load(f)

    with open(thr_file) as f:
        threshold = json.load(f)

    for venue_id, threshold_info in threshold.items():
        # thresholdファイルの項目順に検査
        name = threshold_info['name']
        checkin_stat = stats['statistics'].get(venue_id)
        if checkin_stat:
            count = checkin_stat['count']
            d = datetime.datetime.strptime(checkin_stat['latest'], '%Y-%m-%d %H:%M:%S')
            latest = d.strftime('%Y/%m/%d')
            d = datetime.datetime.strptime(checkin_stat['oldest'], '%Y-%m-%d %H:%M:%S')
            oldest = d.strftime('%Y/%m/%d')
            print("{},{},{},{}".format(name, count, latest, oldest))
        else:
            print("{},{},{},{}".format(name, "", "", ""))

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--stat", help="stat file")
    p.add_argument("--threshold", help="threshold configure file")
    args = p.parse_args()

    stat_file = args.stat or statistics_file
    thr_file = args.threshold or threshold_file

    statistics(stat_file, thr_file)

    # with open(out_file, mode='w') as f:
    #     f.write(json.dumps(data, ensure_ascii=False, indent=2))
