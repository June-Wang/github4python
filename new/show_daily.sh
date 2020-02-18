#!/bin/bash

#VIRTUAL_ENV_DISABLE_PROMPT=1
source ~/.env/bin/activate

/home/wangxj/bin/show_daily.py |grep 'tushare_pro' > /tmp/info.txt

sleep 10s

test -f /tmp/info.txt &&\
curl -i -XPOST 'http://localhost:8086/write?db=stock&u=stock_admin&p=Ab2016' --data-binary @/tmp/info.txt

