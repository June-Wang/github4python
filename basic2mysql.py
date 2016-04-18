#!/usr/bin/env python3.4

import sys
import tushare as ts
from sqlalchemy import create_engine
import mysql.connector

df = ts.get_tick_data('600848', date='2014-12-22')
#engine = create_engine('mysql://stockadmin:stock2016@127.0.0.1/stock?charset=utf8')
conn = create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock?charset=utf8')

try:
#存入数据库
    df.to_sql('tick_data',conn)
except mysql.connector.errors.ProgrammingErro as msg:
    print(msg)
    sys.exit(1)

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')
