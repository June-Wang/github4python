#!/bin/bash

tmp="/tmp/coll.$$"
#SET EXIT STATUS AND COMMAND
trap "exit 1"           HUP INT PIPE QUIT TERM
trap "test -f ${tmp} && rm -f ${tmp}"  EXIT

VIRTUAL_ENV_DISABLE_PROMPT=1
source ~/.env/bin/activate

cd ~/github4python/influx &&\
./coll_stock.py > ${tmp}

test -s ${tmp} &&\
curl -i -XPOST 'http://localhost:8086/write?db=stock&u=stock_admin&p=Ab2016' --data-binary @${tmp}
