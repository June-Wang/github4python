#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd
import time

df_basics = ts.get_stock_basics()
#code,代码
#name,名称
#industry,所属行业
#area,地区
#pe,市盈率
#outstanding,流通股本
#totals,总股本(万)
#totalAssets,总资产(万)
#liquidAssets,流动资产
#fixedAssets,固定资产
#reserved,公积金
#reservedPerShare,每股公积金
#eps,每股收益
#bvps,每股净资
#pb,市净率
#timeToMarket,上市日期

#df_basics_list = list(df_basics[df_basics.totals < 500000].index)
df_basics_list = list(df_basics[df_basics.totals >0].index)

df_profit = ts.get_profit_data(2015,4)
#code,代码
#name,名称
#roe,净资产收益率(%)
#net_profit_ratio,净利率(%)
#gross_profit_rate,毛利率(%)
#net_profits,净利润(万元)
#eps,每股收益
#business_income,营业收入(百万元)
#bips,每股主营业务收入(元)

df_profit_list = list(df_profit[df_profit.gross_profit_rate>=30][df_profit.roe >=5].code)

df_growth = ts.get_growth_data(2015,4)
#code,代码
#name,名称
#mbrg,主营业务收入增长率(%)
#nprg,净利润增长率(%)
#nav,净资产增长率
#targ,总资产增长率
#epsg,每股收益增长率
#seg,股东权益增长率

#growth = df_growth[df_growth.mbrg >0][df_growth.nprg >0][df_growth.nav>0][df_growth.targ>0][df_growth.epsg>0][df_growth.seg>0].code
df_growth_list = list(df_growth[df_growth.mbrg >= 90][df_growth.nprg >0].code)

df_today = ts.get_today_all()
#code：代码
#name:名称
#changepercent:涨跌幅
#trade:现价
#open:开盘价
#high:最高价
#low:最低价
#settlement:昨日收盘价
#volume:成交量
#turnoverratio:换手率

df_price_list = list(df_today[df_today.trade < 15][df_today.trade >0].code)

code_list = list()
#df_basics_list
for code in [df_price_list,df_profit_list,df_growth_list]:
    code_list.extend(code)

print("\n")
num=0
for code in set(code_list):
    count = code_list.count(code)
    if count == 3:
        price_close = df_today[df_today.code == code].trade.values[0]
        stock = df_growth[df_growth.code == code]
        stock_basics = df_basics[df_basics.index == code]
        stock_code = str(stock.code.values[0])
        stock_name = str(stock.name.values[0])
        stock_close = str("%.2f" % price_close)
        stock_industry = str(stock_basics.industry.values[0])
        stock_mbrg = str(stock.mbrg.values[0])
        print(stock_code+"\t"+stock_name+"\t"+stock_close+"\t"+stock_industry+"\t"+stock_mbrg)
        num+=1
        #time.sleep(1)
print(num)
