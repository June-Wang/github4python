#!/bin/bash

for i in `seq 600`
do
	date_20days=`echo $i+20|bc`
	date_10days=`echo $i+10|bc`
	date_yestday=`echo $i+1|bc`
	date_3week_ago=`date -d -${date_20days}day +"%Y-%m-%d"`
	date_10days_ago=`date -d -${date_10days}day +"%Y-%m-%d"`
	date_yestday_time=`date -d -${date_yestday}day +"%Y-%m-%d"`
	my_day=`date -d -${i}day +"%Y-%m-%d"`
	python3 check_stock_000998.py "${my_day}" "${date_3week_ago}" "${date_10days_ago}" "${date_yestday_time}">> ./final.txt
done
