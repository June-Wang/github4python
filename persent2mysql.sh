#!/bin/bash

VIRTUAL_ENV_DISABLE_PROMPT=1
source ~/.env/bin/activate

cd ~/github4python/ &&\
./persent2mysql.py >/dev/null 2>&1
