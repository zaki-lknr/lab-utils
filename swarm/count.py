import json
import datetime
import argparse

threshold_file = 'threshold.json'
statistics_file = 'logs/stat.json'
result_file = 'result.log'
today_file = ''

def statistics(stat_file, thr_file):
    result = []

    with open(stat_file) as f:
        stats = json.load(f)

    with open(thr_file) as f:
        threshold = json.load(f)

    for venue_id, threshold_info in threshold.items():
        # thresholdファイルの項目順に検査
        name = threshold_info['name']
        count_threshold = threshold_info['count']
        interval_threshold = threshold_info['threshold']
        checkin_stat = stats['statistics'].get(venue_id)
        if checkin_stat:
            count = checkin_stat['count']
            interval = checkin_stat['passed']
            d = datetime.datetime.strptime(checkin_stat['latest'], '%Y-%m-%d %H:%M:%S')
            latest = d.strftime('%Y/%m/%d')
            d = datetime.datetime.strptime(checkin_stat['oldest'], '%Y-%m-%d %H:%M:%S')
            oldest = d.strftime('%Y/%m/%d')
            mayor = '' if (checkin_stat['mayor']) else 'x'
            result.append("{},{},{},{},{},{},{},{}".format(name, mayor, count, count_threshold, latest, interval, interval_threshold, oldest))
        else:
            result.append("{},{},{},{},{},{},{},{}".format(name, "", "", count_threshold, "", "", interval_threshold, ""))
    return result

def get_today_count(checkins_list):
    count = 0
    with open(checkins_list) as f:
        d = json.load(f)
        checkin = checkins = d['response']['checkins']['items']
        today_datetime = datetime.datetime.now()

        for checkin in checkins:
            checkin_datetime = datetime.datetime.fromtimestamp(checkin['createdAt'])
            if (checkin_datetime.date() == today_datetime.date()):
                count += 1

    return count

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--stat", help="stat file")
    p.add_argument("--threshold", help="threshold configure file")
    p.add_argument("--out", help="output file")
    p.add_argument("--today", help="today checkins list file")
    args = p.parse_args()

    stat_file = args.stat or statistics_file
    thr_file = args.threshold or threshold_file
    out_file = args.out or result_file
    today_file = args.today or today_file

    r = statistics(stat_file, thr_file)
    count = get_today_count(today_file)

    with open(out_file, mode='w') as f:
        f.write("\n".join(r))
        f.write("\n\n" + str(count) + "\n")
