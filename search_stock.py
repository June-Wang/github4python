#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd

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

df_basics_list = df_basics[df_basics.totals < 1000000000].code

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

df_profit_list = df_profit[df_profit.gross_profit_rate > 40 ].code

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
df_growth_list = df_growth[df_growth.mbrg >0][df_growth.nprg >0].code

code_list = sorted(list(set(profit).intersection(set(growth))))

for code in code_list:
	rows = df_growth[df_growth.code == code][['code','name']]
	print(rows.code.values,rows.name.values)
