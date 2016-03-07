#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd

stock_code = sys.argv[1]
stock_code_p_change = float(sys.argv[2])

num4days = 200
now = datetime.date.today()
yestoday = now - datetime.timedelta(days=1)
date_ago = now - datetime.timedelta(days=num4days)

before_yestoday = now - datetime.timedelta(days=2)
before_date_ago = now - datetime.timedelta(days=num4days+1)

for1day = reversed(pd.bdate_range(start=str(date_ago),end=str(yestoday)))
for2day = reversed(pd.bdate_range(start=str(before_date_ago),end=str(before_yestoday)))

df = ts.get_hist_data(stock_code,start=str(before_date_ago),end=str(yestoday))

#my_days = set(df.index)
#my_days = reversed(sorted(set(df.index)))

for day in for1day:
	try:
		price = df[df.index == str(day.date())].close[0]
	except:
		continue

	if price != price:
		continue
	volume = df.volume[0]
	price_min = df.low[0]
	price_max = df.high[0]
	price_avg_5 = df.ma5[0]
	price_avg_10 = df.ma10[0]
	price_avg_20 = df.ma20[0]
	p_change = df.p_change[0]
	p_change_avg_5 = (price - price_avg_5)/price_avg_5 * 100
	p_change_avg_10 = (price - price_avg_10)/price_avg_10 * 100
	p_change_avg_20 = (price - price_avg_20)/price_avg_20 * 100

	act_msg = ''
	#my_date = now - datetime.timedelta(days=num)
	my_date = str(day)
	date_now = str(my_date)
	price_msg = 'price(1/5/10/20/min/max):\t'+("%.2f" % price)+'\t'+("%.2f" % price_avg_5)+'\t'+("%.2f" % price_avg_10)+'\t'+("%.2f" % price_avg_20)+'\t'+("%.2f" % price_min)+'\t'+("%.2f" % price_max)
	p_change_msg = 'change(1/5/10):\t'+("%.2f" % p_change)+'\t'+("%.2f" % p_change_avg_5)+'\t'+("%.2f" % p_change_avg_10)#+'\t'+("%.2f" % p_change_avg_20)
	print(date_now+' '+price_msg+' '+p_change_msg+'\t'+ ' '+act_msg)
