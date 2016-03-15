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
end_day = now - datetime.timedelta(days=num4days)
workday = pd.bdate_range(start=str(end_day),end=str(yestoday))

try:
	df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
except:
	print('timeout!')
	sys.exit(1)	

days = len(workday.date)

for i in range(days-1,10,-1):
	my_str = ''
	date_today = str(workday.date[i])
	date_yestoday = str(workday.date[i-1])
	date_now = date_today

	try:
		price_open = df[df.index == date_today].open[0]
		yestoday_price_open = df[df.index == date_yestoday].open[0]
	except:
		#print(date_now,'no data!')	
		continue

	if price_open != price_open:
		continue

	volume = df[df.index == date_today].volume[0]
	price_open = df[df.index == date_today].open[0]
	price_close = df[df.index == date_today].close[0]
	price_min = df[df.index == date_today].low[0]
	price_max = df[df.index == date_today].high[0]
	price_avg_5 = df[df.index == date_today].ma5[0]
	price_avg_10 = df[df.index == date_today].ma10[0]
	price_avg_20 = df[df.index == date_today].ma20[0]

	p_change_3 = 0.0
	for f3 in range(i-1,i-4,-1):
		my_date = str(workday.date[f3])
		try:
			my_change = float(df[df.index == my_date].p_change[0])
		except:
			my_change = 0.0
		p_change_3 = p_change_3 + my_change

	p_change_5 = 0.0
	for f5 in range(i-1,i-6,-1):
		my_date = str(workday.date[f5])
		try:
			my_change = float(df[df.index == my_date].p_change[0])
		except:
			my_change = 0.0
		p_change_5 = p_change_5 + my_change

	p_change_10 = 0.0
	for f10 in range(i-1,i-11,-1):
		my_date = str(workday.date[f10])
		try:
			my_change = float(df[df.index == my_date].p_change[0])
		except:
			my_change = 0.0
		p_change_10 = p_change_10 + my_change

	p_change = df[df.index == date_today].p_change[0]
	p_change_min = (price_min - price_open)/price_open * 100
	p_change_max = (price_max - price_open)/price_open * 100
	p_change_open = p_change_max + p_change_min
	p_change_close = (price_min - price_close)/price_close * 100 + (price_max - price_close)/price_close * 100
	p_change_avg_5 = (price_close - price_avg_5)/price_avg_5 * 100
	p_change_avg_10 = (price_close - price_avg_10)/price_avg_10 * 100
	p_change_avg_20 = (price_close - price_avg_20)/price_avg_20 * 100

	yestoday_price_open = df[df.index == date_yestoday].open[0]
	yestoday_price_close = df[df.index == date_yestoday].close[0]
	yestoday_price_avg_5 = df[df.index == date_yestoday].ma5[0]
	yestoday_price_avg_10 = df[df.index == date_yestoday].ma10[0]
	yestoday_p_change_avg_5 = (yestoday_price_close - yestoday_price_avg_5)/yestoday_price_avg_5 * 100
	yestoday_p_change_avg_10 = (yestoday_price_close - yestoday_price_avg_10)/yestoday_price_avg_10 * 100
	
#	if p_change > p_change_avg_10 and p_change_avg_5 < 0 and p_change > p_change_avg_5 and p_change_avg_5 > p_change_avg_10 and  yestoday_p_change_avg_10 <= (stock_code_p_change*-1) and p_change_avg_10 > yestoday_p_change_avg_10:

	price_msg = 'price(open/close/5/10/min/max):\t'+("%.2f" % price_open)+'\t'+("%.2f" % price_close)+'\t'+("%.2f" % price_avg_5)+'\t'+("%.2f" % price_avg_10)+'\t'+("%.2f" % price_min)+'\t'+("%.2f" % price_max)
	p_change_msg = 'change(1/5/10/open/close/min/max):\t'+("%.2f" % p_change)+'\t'+("%.2f" % p_change_avg_5)+'\t'+("%.2f" % p_change_avg_10)+'\t'+("%.2f" % p_change_open) +'\t'+("%.2f" % p_change_close)+'\t'+("%.2f" % p_change_min) +'\t'+("%.2f" % p_change_max) 
	p_change_msg = 'change(1/3/5/10):\t'+("%.2f" % p_change)+'\t'+("%.2f" % p_change_3)+'\t'+("%.2f" % p_change_5)+'\t'+("%.2f" % p_change_10)#+'\t'+("%.2f" % p_change_open) +'\t'+("%.2f" % p_change_close)+'\t'+("%.2f" % p_change_min) +'\t'+("%.2f" % p_change_max) 
	
	if p_change_min < -6 and p_change_avg_5 < -5 and price_avg_10 > price_open:
		print(Fore.YELLOW+date_now+' '+price_msg+' '+p_change_msg+Style.RESET_ALL)
	elif p_change_max < 1 and p_change_max > -1 and p_change < -4 and  p_change_min < -4:
		print(Fore.CYAN+date_now+' '+price_msg+' '+p_change_msg+Style.RESET_ALL)
	elif p_change > 0:
		print(Fore.RED+date_now+' '+price_msg+' '+p_change_msg+Style.RESET_ALL)
	elif p_change < 0:
		print(Fore.GREEN+date_now+' '+price_msg+' '+p_change_msg+Style.RESET_ALL)
	else:
		print(date_now+' '+price_msg+' '+p_change_msg)
