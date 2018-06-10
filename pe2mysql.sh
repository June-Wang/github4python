#!/bin/bash

VIRTUAL_ENV_DISABLE_PROMPT=1
source ~/.env/bin/activate

cd ~/github4python/ &&\
./pe2mysql.py >/tmp/pe.log 2>&1
