#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd

stock_code = sys.argv[1]
now = datetime.date.today()
yestoday = now - datetime.timedelta(days=1)
tenday = now - datetime.timedelta(days=10)

try:
    df = ts.get_hist_data(stock_code,start=str(tenday),end=str(yestoday))
except:
    print('timeout!')
    sys.exit(1)

price_close = ("%.2f" % df.close[0])

if price_close:
	print('code: '+stock_code+' price: '+price_close+'.| price_close='+price_close+';;;')
