#!/bin/bash

for i in `seq 180`
do
	days=`echo $i+21|bc`
	date_3week_ago=`date -d -${days}day +"%Y-%m-%d"`
	my_day=`date -d -${i}day +"%Y-%m-%d"`
	python3 check_stock_000998.py "${my_day}" "${date_3week_ago}" >> ./final.txt
done
