#!/usr/bin/env python3.4

import sys
import time
import tushare as ts
import sqlalchemy as sa
import mysql.connector

try:
    year = sys.argv[1]
except:
    print('year not null!')
    sys.exit(1)

if not year:
    print('year not null!')
    sys.exit(1)

#year = '2016'
conn = sa.create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock')

#profit_sql = '''select code from profit where net_profit_ratio >=30 and gross_profit_rate >=30 and roe >=5 and year = %s group by code;'''
profit_sql = '''select code from profit where net_profit_ratio >=30 and gross_profit_rate >=30 and year = %s group by code;'''
rows = conn.execute(profit_sql,year)

#profit_list = [row.values() for row in rows]
profit_list = list()
for row in rows:
    profit_list.extend(row.values())

#print(profit_list)

stock_name_sql = '''select code,name,industry from list;'''
rows = conn.execute(stock_name_sql)

stock_name = dict()
stock_industry = dict()
for code,name,industry in rows:
    stock_name[code] = name
    stock_industry[code] = industry
#    print(code,name)
#sys.exit(0)

growth_sql = '''select code from growth where mbrg>90 and nprg >0 and  year = %s group by code;'''
rows = conn.execute(growth_sql,year)

growth_list = list()
for row in rows:
    growth_list.extend(row.values())
#print(growth_list)

#df_basics = ts.get_stock_basics()
#df_basics_list = list(df_basics[df_basics.totals >0].index)
#time.sleep(5)
#df_today = ts.get_today_all()

today_sql = '''select code,trade from today group by code;'''
rows = conn.execute(today_sql)

stock_price = dict()
for code,price in rows:
    stock_price[code] = price

code_list = list()
for code in [profit_list,growth_list]:
    code_list.extend(code)

for code in sorted(set(code_list)):
    count = code_list.count(code)
    if count == 2 and stock_price[code] >0:
        print('\t'.join([code,stock_name[code],stock_industry[code],str(stock_price[code])]))
