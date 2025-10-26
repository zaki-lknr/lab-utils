#!/bin/bash

yyyymmdd_yesterday=$(date +%Y%m%d -d -1day)
yyyymmdd=$(date +%Y%m%d)
mmdd=$(date +%m%d)

# workdir=
# devdir=

today_log=${devdir}/logs/user-checkin-${mmdd}.json
all_log=${workdir}/logs/all-checkins-${yyyymmdd}.json
all_yesterday=${workdir}/logs/all-checkins-${yyyymmdd_yesterday}.json

${devdir}/get-user-checkins.sh \
    > ${today_log}

python ${workdir}/marge-log.py \
    --base ${all_yesterday} \
    --add ${today_log} \
    --out ${all_log}

python ${workdir}/calc.py \
    --src ${all_log} \
    --out ${workdir}/logs/stat${mmdd}.json \
    --threshold ${workdir}/threshold.json

python ${workdir}/count.py \
    --stat ${workdir}/logs/stat${mmdd}.json \
    --threshold ${workdir}/threshold.json \
    --out ${workdir}/logs/stat${mmdd}.csv

#TODO: 変数定義のバラツキを修正する
