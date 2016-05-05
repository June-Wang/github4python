#!/usr/bin/env python3.4

import sys
import time
import tushare as ts
from sqlalchemy import create_engine
import mysql.connector

try:
    df = ts.get_today_all()
except:
    print('time out!')
    sys.exit(1)

conn = create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock?charset=utf8')

sql = '''DROP TABLE IF EXISTS `today`;'''
conn.execute(sql)

sql = '''CREATE TABLE `today` (
  `index` bigint DEFAULT NULL,
  `code` char(6) DEFAULT NULL,
  `name` varchar(20) DEFAULT NULL,
  `changepercent` double DEFAULT NULL,
  `trade` double DEFAULT NULL,
  `open` double DEFAULT NULL,
  `high` double DEFAULT NULL,
  `low` double DEFAULT NULL,
  `settlement` double DEFAULT NULL,
  `volume` double DEFAULT NULL,
  `turnoverratio` double DEFAULT NULL,
  `amount` double DEFAULT NULL,
  `per` double DEFAULT NULL,
  `pb` double DEFAULT NULL,
  `mktcap` double DEFAULT NULL,
  `nmc` double DEFAULT NULL,
  PRIMARY KEY (`index`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''
conn.execute(sql)

df.to_sql('today',conn,if_exists='append')
