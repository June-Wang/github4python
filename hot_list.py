#!/usr/bin/env python3.4

import sys
import tushare as ts

my_year = sys.argv[1]
df = ts.profit_data(top=100,year=my_year)
hot = df.sort_values('shares',ascending=False).head(20)
print("\n配股排名\n",hot)
hot = df.sort_values('divi',ascending=False).head(20)
print("\n分红排名\n",hot)
