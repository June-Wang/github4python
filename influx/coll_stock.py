#!/usr/bin/env python3

import sys,re,os,datetime,time
import tushare as ts

#timestamp = str(time.time()).replace('.','')
df = ts.get_realtime_quotes(['000998','600188','600519'])
for i in range(len(df)):
    price = float(df[['price']].values[i][0])
    pre_close = float(df[['pre_close']].values[i][0])
    per_persent = (price - pre_close)/pre_close * 100
    code = df[['code']].values[i][0]
    name = df[['name']].values[i][0]
    msg = """stock_realtime_persent,code=%s,name=%s per_persent=%s"""
    message = msg % (code,name,("%.2f" % per_persent))
    print(message)
