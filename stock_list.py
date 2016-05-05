#!/usr/bin/env python3.4

import sys
import time
import tushare as ts
from sqlalchemy import create_engine
import mysql.connector

try:
    df = ts.get_stock_basics()
except:
    print('time out!')
    sys.exit(1)

conn = create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock?charset=utf8')

sql = '''DROP TABLE IF EXISTS `list`;'''
conn.execute(sql)

sql = '''CREATE TABLE `list` (
  `code` char(6),
  `name` varchar(20),
  `industry` varchar(20),
  `area` varchar(10),
  `pe` double DEFAULT NULL,
  `outstanding` double DEFAULT NULL,
  `totals` double DEFAULT NULL,
  `totalAssets` double DEFAULT NULL,
  `liquidAssets` double DEFAULT NULL,
  `fixedAssets` double DEFAULT NULL,
  `reserved` double DEFAULT NULL,
  `reservedPerShare` double DEFAULT NULL,
  `esp` double DEFAULT NULL,
  `bvps` double DEFAULT NULL,
  `pb` double DEFAULT NULL,
  `timeToMarket` bigint(20) DEFAULT NULL,
  PRIMARY KEY (`code`),
  UNIQUE KEY `code_name` (`code`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
'''
conn.execute(sql)

df.to_sql('list',conn,if_exists='append')
