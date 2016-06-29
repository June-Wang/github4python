#!/bin/bash

file="$1"
cat ${file} |\
while read code name
do 
	grep "${code}" ./nxx.list >/dev/null &&\
	echo "${code} ${name}"
done
