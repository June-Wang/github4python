#!/bin/bash

VIRTUAL_ENV_DISABLE_PROMPT=1
source ~/.env/bin/activate

cd ~/github4python/ &&\
./overview2influx.py >/dev/null 2>&1
