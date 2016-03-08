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

day_today = pd.bdate_range(start=str(date_ago),end=str(yestoday))
day_yestoday = pd.bdate_range(start=str(before_date_ago),end=str(before_yestoday))

today_list = list()
yestoday_list = list()

for day in day_today:
	today_list.append(str(day.date()))

for day in day_yestoday:
	yestoday_list.append(str(day.date()))

#sys.exit(1)

df = ts.get_hist_data(stock_code,start=str(date_ago),end=str(yestoday))

#for day in reversed(day_today):
for day in today_list:
	date_today = today_list.pop()
	date_yestoday = yestoday_list.pop()

	try:
		price = df[df.index == date_today].close[0]
		yestoday_price = df[df.index == date_yestoday].close[0]
	except:
		continue

	if price != price:
		continue

	volume = df[df.index == date_today].volume[0]
	price_min = df[df.index == date_today].low[0]
	price_max = df[df.index == date_today].high[0]
	price_avg_5 = df[df.index == date_today].ma5[0]
	price_avg_10 = df[df.index == date_today].ma10[0]
	price_avg_20 = df[df.index == date_today].ma20[0]
	p_change = df[df.index == date_today].p_change[0]
	p_change_avg_5 = (price - price_avg_5)/price_avg_5 * 100
	p_change_avg_10 = (price - price_avg_10)/price_avg_10 * 100
	p_change_avg_20 = (price - price_avg_20)/price_avg_20 * 100

	yestoday_price_avg_5 = df[df.index == date_yestoday].ma5[0]
	yestoday_price_avg_10 = df[df.index == date_yestoday].ma10[0]
	yestoday_p_change_avg_5 = (yestoday_price - yestoday_price_avg_5)/yestoday_price_avg_5 * 100
	yestoday_p_change_avg_10 = (yestoday_price - yestoday_price_avg_10)/yestoday_price_avg_10 * 100
	
	#print(date_today,date_yestoday)
	#continue

	act_msg = ''
	date_now = date_today
	price_msg = 'price(1/5/10/20/min/max):\t'+("%.2f" % price)+'\t'+("%.2f" % price_avg_5)+'\t'+("%.2f" % price_avg_10)+'\t'+("%.2f" % price_avg_20)+'\t'+("%.2f" % price_min)+'\t'+("%.2f" % price_max)
	p_change_msg = 'change(1/5/10):\t'+("%.2f" % p_change)+'\t'+("%.2f" % p_change_avg_5)+'\t'+("%.2f" % p_change_avg_10)#+'\t'+("%.2f" % p_change_avg_20)
	print(date_now+' '+price_msg+' '+p_change_msg+'\t'+ ' '+act_msg)
