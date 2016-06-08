#!/bin/bash

cat new |\
while read code name
do 
	grep "${code}" ./nxx.list >/dev/null &&\
	echo "${code} ${name}"
done
