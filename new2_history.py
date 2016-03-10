#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd
import colorama
from colorama import Fore, Back, Style

colorama.init()

stock_code = sys.argv[1]
stock_code_p_change = float(sys.argv[2])

num4days = 100
now = datetime.date.today()
yestoday = now - datetime.timedelta(days=1)
date_ago = now - datetime.timedelta(days=num4days)

day_today = pd.bdate_range(start=str(date_ago),end=str(yestoday))

try:
	df = ts.get_hist_data(stock_code,start=str(date_ago),end=str(yestoday))
except:
	print('timeout!')
	sys.exit(1)	

days = len(day_today.date)

for i in range(days-1,0,-1):
	date_today = str(day_today.date[i])
	date_yestoday = str(day_today.date[i-1])
	#print(str(date_today),date_yestoday)

	try:
		price = df[df.index == date_today].close[0]
		yestoday_price = df[df.index == date_yestoday].close[0]
	except:
		continue

	if price != price:
		continue

	volume = df[df.index == date_today].volume[0]
	price_open = df[df.index == date_today].open[0]
	price_min = df[df.index == date_today].low[0]
	price_max = df[df.index == date_today].high[0]

	p_change_min = (price_min - price_open)/price_open * 100
	p_change_max = (price_max - price_open)/price_open * 100
	#p_change_open = (price_max - price_min)/price_open * 100
	p_change_open = p_change_max + p_change_min

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

#	if p_change > p_change_avg_10 and p_change_avg_5 < 0 and p_change > p_change_avg_5 and p_change_avg_5 > p_change_avg_10 and  yestoday_p_change_avg_10 <= (stock_code_p_change*-1) and p_change_avg_10 > yestoday_p_change_avg_10:

	date_now = date_today
	price_msg = 'price(1/5/10/min/max):\t'+("%.2f" % price)+'\t'+("%.2f" % price_avg_5)+'\t'+("%.2f" % price_avg_10)+'\t'+("%.2f" % price_min)+'\t'+("%.2f" % price_max)
	p_change_msg = 'change(1/5/10/open/min/max):\t'+("%.2f" % p_change)+'\t'+("%.2f" % p_change_avg_5)+'\t'+("%.2f" % p_change_avg_10)+'\t'+("%.2f" % p_change_open) +'\t'+("%.2f" % p_change_min) +'\t'+("%.2f" % p_change_max) #+'\t'+("%.2f" % p_change_avg_20)
	if p_change_min < -6 and p_change_avg_5 < -5:
		print(Fore.GREEN+date_now+' '+price_msg+' '+p_change_msg+Style.RESET_ALL)
	else:
		print(date_now+' '+price_msg+' '+p_change_msg)
