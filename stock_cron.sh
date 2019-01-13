#!/bin/bash

VIRTUAL_ENV_DISABLE_PROMPT=1
source ~/.env/bin/activate

cd ~/github4python/ &&\
./stock_cron.py|\
grep -E '^stock_cron'|\
xargs -r -i curl -i -XPOST 'http://localhost:8086/write?db=stock&u=stock_admin&p=Ab2016' --data-binary "{} `date -d now +'%s%N'`"
