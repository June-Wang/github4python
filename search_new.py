#!/usr/bin/env python3.4

import sys
import time
import tushare as ts
import sqlalchemy as sa
import mysql.connector

year = '2014'
conn = sa.create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock')

#
profit_sql = '''select code from profit where net_profit_ratio >=30 and gross_profit_rate >=30 and roe >=5 and year = %s group by code;'''
rows = conn.execute(profit_sql,year)

#profit_list = [row.values() for row in rows]
profit_list = list()
for row in rows:
    profit_list.extend(row.values())

#print(profit_list)

stock_name_sql = '''select code,name from profit where year = %s group by code;'''
rows = conn.execute(stock_name_sql,year)

stock_dict = dict()
for code,name in rows:
    stock_dict[code] = name
#    print(code,name)
#sys.exit(0)

growth_sql = '''select code from growth where mbrg>90 and nprg >0 and  year = %s group by code;'''
rows = conn.execute(growth_sql,year)

growth_list = list()
for row in rows:
    growth_list.extend(row.values())
#print(growth_list)

df_basics = ts.get_stock_basics()
df_basics_list = list(df_basics[df_basics.totals >0].index)
time.sleep(5)
df_today = ts.get_today_all()

code_list = list()
for code in [profit_list,growth_list,df_basics_list]:
    code_list.extend(code)


for code in set(code_list):
    count = code_list.count(code)
    price = df_today[df_today.code == code].trade.values
    if count == 3 and price >0:
    #if count == 2:
        stock_basics = df_basics[df_basics.index == code]
        stock_industry = str(stock_basics.industry.values[0])
        print(code,stock_dict[code],price,stock_industry)
