#!/bin/bash

search_list="$1"
for good_list in share.list short.list 
do
#good_list="$1"
	cat ${good_list}|grep -oP '\d{6}'|\
	while read code
	do 
		grep "${code}" ${search_list}
		#echo "${code} ${name}"
	done
done
