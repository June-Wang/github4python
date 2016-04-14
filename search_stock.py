#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd

df_profit = ts.get_profit_data(2015,4)

df_growth = ts.get_growth_data(2015,4)

profit = df_profit[df_profit.roe >15].code

#growth = df_growth[df_growth.mbrg >0][df_growth.nprg >0][df_growth.nav>0][df_growth.targ>0][df_growth.epsg>0][df_growth.seg>0].code
growth = df_growth[df_growth.mbrg >0][df_growth.nprg >0].code

code_list = sorted(list(set(profit).intersection(set(growth))))

for code in code_list:
	rows = df_growth[df_growth.code == code][['code','name']]
	print(rows.code.values,rows.name.values)
