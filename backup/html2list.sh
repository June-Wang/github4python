#!/bin/bash

file="$1"

test -f ${file} ||\
eval "echo ${file} not found!;exit 1"

grep -oP 's[z|h]\d{6}' ${file}|sort -u|grep -v sh000001|sed 's/^..//'|sort
