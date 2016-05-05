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

stock_name_sql = '''select code,name,industry from list;'''
rows = conn.execute(stock_name_sql)

stock_name = dict()
stock_industry = dict()
for code,name,industry in rows:
    stock_name[code] = name
    stock_industry[code] = industry

today_sql = '''select code,trade from today group by code;'''
rows = conn.execute(today_sql)

stock_price = dict()
for code,price in rows:
    stock_price[code] = price

profit_sql = '''select code,sum(net_profit_ratio),sum(gross_profit_rate),sum(roe),count(*) from profit where year = %s group by code;'''
rows = conn.execute(profit_sql,year)

profit_list = list()
for code,net_profit_ratio,gross_profit_rate,roe,count in rows:
    net_profit_ratio_avg = net_profit_ratio/count
    gross_profit_rate_avg = gross_profit_rate/count
    roe_avg = roe/count
    #if net_profit_ratio_avg >= 40 and gross_profit_rate_avg >= 40:
    if net_profit_ratio_avg >= 40 and gross_profit_rate_avg >= 45 and roe_avg >=0:
        profit_list.append(code)

growth_sql = '''select code,sum(mbrg),sum(nprg),sum(nav),sum(targ),sum(epsg),sum(seg),count(*) from growth where year = %s group by code'''
rows = conn.execute(growth_sql,year)

growth_list = list()
for code,mbrg,nprg,nav,targ,epsg,seg,count in rows:
    mbrg_avg = mbrg/count
    nprg_avg = nprg/count
    nav_avg = nav/count
    targ_avg = targ/count
    epsg_avg = epsg/count
    seg_avg = seg/count
    #if mbrg_avg >= 80:
    if mbrg_avg > 30 and nprg_avg > 0 and nav_avg >0 and epsg_avg >0:
        growth_list.append(code)

Market_Cap_sql = '''select today.code,today.trade,list.totals from today,list where today.code=list.code'''
rows = conn.execute(Market_Cap_sql)

Market_Cap_list = list()
Market_Cap_dict = dict()
for code,trade,totals in rows:
    Market_Cap = trade*totals/10000 #亿
    if Market_Cap < 1000:
        Market_Cap_dict[code] = Market_Cap
        Market_Cap_list.append(code)

code_list = list()
for code in [profit_list,growth_list,Market_Cap_list]:
    code_list.extend(code)

for code in sorted(set(code_list)):
    count = code_list.count(code)
    if code not in stock_price:
        continue
    if count == 3 and stock_price[code] >0:
        print('\t'.join([code,stock_name[code],stock_industry[code],("%.2f" % stock_price[code]),("%.2f" % Market_Cap_dict[code])]))
