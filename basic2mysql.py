#!/usr/bin/env python3.4

import sys
import time
import tushare as ts
from sqlalchemy import create_engine
import mysql.connector

conn = create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock?charset=utf8')

for year in range(2014,2016):
    for season in  range(1,5):
        print(year,season)
        df_profit = ts.get_profit_data(year,season)
        time.sleep(15)
        df_growth = ts.get_growth_data(year,season)
        time.sleep(15)
        df_operation = ts.get_operation_data(year,season)
        time.sleep(15)
        df_debtpaying = ts.get_debtpaying_data(year,season)
        time.sleep(15)
        df_cashflow = ts.get_cashflow_data(year,season)
        time.sleep(15)
        df_report = ts.get_report_data(year,season)
        df_profit.to_sql('profit',conn,if_exists='append')
        df_growth.to_sql('growth',conn,if_exists='append')
        df_operation.to_sql('operation',conn,if_exists='append')
        df_debtpaying.to_sql('debtpaying',conn,if_exists='append')
        df_cashflow.to_sql('cashflow',conn,if_exists='append')
        df_report.to_sql('report',conn,if_exists='append')

#sys.exit(1)

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')
