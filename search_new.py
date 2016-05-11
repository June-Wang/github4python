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

stock_name_sql = '''select code,name,industry,pe from list;'''
rows = conn.execute(stock_name_sql)

stock_list = list()
stock_name = dict()
stock_industry = dict()
stock_pe = dict()
for code,name,industry,pe in rows:
    if pe < 150: #市盈率
        stock_name[code] = name
        stock_industry[code] = industry
        stock_pe[code] = pe
        stock_list.append(code)

today_sql = '''select code,trade from today group by code;'''
rows = conn.execute(today_sql)

stock_price = dict()
for code,price in rows:
    stock_price[code] = price

profit_sql = '''select code,sum(net_profit_ratio),sum(gross_profit_rate),sum(eps),sum(roe),count(*) from profit where year = %s group by code;'''
rows = conn.execute(profit_sql,year)

profit_list = list()
for code,net_profit_ratio,gross_profit_rate,eps,roe,count in rows:
    net_profit_ratio_avg = net_profit_ratio/count #净利率
    gross_profit_rate_avg = gross_profit_rate/count #毛利率
    roe_avg = roe/count #净资产收益率
    eps_avg = eps/count #每股收益
    #if net_profit_ratio_avg >= 40 and gross_profit_rate_avg >= 40:
    if net_profit_ratio_avg >= 30 and gross_profit_rate_avg >= 45 and eps_avg >0 and roe_avg >=5:
    #if net_profit_ratio_avg >= 30 and gross_profit_rate_avg >= 45 and roe_avg >=5:
        profit_list.append(code)

growth_sql = '''select code,sum(mbrg),sum(nprg),sum(nav),sum(targ),sum(epsg),sum(seg),count(*) from growth where year = %s group by code'''
rows = conn.execute(growth_sql,year)

growth_list = list()
for code,mbrg,nprg,nav,targ,epsg,seg,count in rows:
    mbrg_avg = mbrg/count #主营业务收入增长率
    nprg_avg = nprg/count #净利润增长率
    nav_avg = nav/count #净资产增长率
    targ_avg = targ/count #总资产增长率
    epsg_avg = epsg/count #每股收益增长率
    seg_avg = seg/count #股东权益增长率
    if mbrg_avg >= 60 and nprg_avg >0 and count >=0:
    #if mbrg_avg >= 30 and nprg_avg > 0 and nav_avg >0 and epsg_avg >0:
        growth_list.append(code)

Market_Cap_sql = '''select today.code,today.trade,list.totals from today,list where today.code=list.code'''
rows = conn.execute(Market_Cap_sql)

Market_Cap_list = list()
Market_Cap_dict = dict()
for code,trade,totals in rows:
    Market_Cap = trade*totals/10000 #市值（亿）
    totals_b = totals/10000 #总股本（亿）
    if Market_Cap < 50000 and totals_b < 15000:
        Market_Cap_dict[code] = Market_Cap
        Market_Cap_list.append(code)

stock_set = set(stock_list)
profit_set = set(profit_list)
growth_set = set(growth_list)
Market_Cap_set = set(Market_Cap_list)

code_list = list(stock_set & profit_set & growth_set & Market_Cap_set)

for code in sorted(set(code_list)):
    if code not in stock_price:
        continue
    if stock_price[code] >0:
        print('\t'.join([code,stock_name[code],stock_industry[code],("%.2f" % stock_price[code]),("%.2f" % Market_Cap_dict[code]),("%.2f" % stock_pe[code])]))
