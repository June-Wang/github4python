#!/usr/bin/env python3.4

import sys
import time
import tushare as ts
from sqlalchemy import create_engine
import mysql.connector

conn = create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock?charset=utf8')

df = ts.get_stock_basics()
df.to_sql('list',conn,if_exists='append')
