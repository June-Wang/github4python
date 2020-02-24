#!/bin/bash

code="$1"

./newone.py ${code}|\
awk -F',' '/^[0-9]/{print "tushare_lite,ts_code="$2",trade_date="$1" close="$3",weight="$4",vol="$5" "$NF}'
