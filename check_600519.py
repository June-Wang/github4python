#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd
import colorama
from colorama import Fore, Back, Style
from termcolor import colored, cprint

colorama.init()

#stock_code = sys.argv[1]
stock_code = '600519'
#stock_code_p_change = float(sys.argv[2])

num4days = 300
now = datetime.date.today()
yestoday = now - datetime.timedelta(days=1)
end_day = now - datetime.timedelta(days=num4days+60)
workday = pd.bdate_range(start=str(end_day),end=str(yestoday))

try:
	df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
except:
	print('timeout!')
	sys.exit(1)	

days = len(workday.date)

def get_day(day,loop_i):
	global workday
	num = day+1
	my_date_tmp = list()
	for my_day in range(loop_i-1,loop_i-num,-1):
		my_date_tmp.append(str(workday.date[my_day]))
	return(my_date_tmp)

def get_p_change_for_days(date_list):
	global df
	my_change_sum = 0.0
	for my_date in date_list:
		try:
			my_change_tmp = float(df[df.index == my_date].p_change[0])
		except:
			my_change_tmp = 0.0
		my_change_sum += my_change_tmp
	return(my_change_sum)

def get_color(text):
	my_number = float(text)
	if my_number > 0:
		my_text = colored(text, 'red')
	elif my_number < 0:
		text = str(abs(my_number))
		my_text = colored(text, 'green')
	else:
		my_text = text
	return(my_text)

#mt_str = 'hello'
#print(get_color(mt_str))
#sys.exit(1)	
			
for i in range(days-1,60,-1):
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

	p_change_3 = get_p_change_for_days(get_day(3,i))
	p_change_5 = get_p_change_for_days(get_day(5,i))
	#p_change_7 = get_p_change_for_days(get_day(7,i))
	p_change_10 = get_p_change_for_days(get_day(10,i))
	p_change_15 = get_p_change_for_days(get_day(15,i))
	p_change_20 = get_p_change_for_days(get_day(20,i))
	p_change_30 = get_p_change_for_days(get_day(30,i))
	p_change_60 = get_p_change_for_days(get_day(60,i))
	p_change_90 = get_p_change_for_days(get_day(90,i))
	p_change_120 = get_p_change_for_days(get_day(120,i))
	p_change_160 = get_p_change_for_days(get_day(160,i))

	p_change = df[df.index == date_today].p_change[0]
	#p_change = df[df.index == date_yestoday].p_change[0]
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
	
	price_msg = 'prix(min/max): '+("%.2f" % price_min)+' '+("%.2f" % price_max)
	
	p_change_title = 'ch(1/3/5/10/15/20/30/60/90/120/160):\t'
	p_change_msg = get_color(("%.2f" % p_change))+'\t'+get_color(("%.2f" % p_change_3))+'\t'+get_color(("%.2f" % p_change_5))+'\t'+get_color(("%.2f" % p_change_10))+'\t'+get_color(("%.2f" % p_change_15))+'\t'+get_color(("%.2f" % p_change_20))+'\t'+get_color(("%.2f" % p_change_30))+'\t'+get_color(("%.2f" % p_change_60))+'\t'+get_color(("%.2f" % p_change_90))+'\t'+get_color(("%.2f" % p_change_120))+'\t'+get_color(("%.2f" % p_change_160))
	
	if p_change_3 < 0 and p_change_5 < 0 and p_change_10 < 0 and p_change_15 <0 and p_change_20 <0 and p_change_30 <0 and p_change_60 <0:
		print(Fore.CYAN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	elif p_change < 0 and p_change_3 > 0 and p_change_5 > 0 and p_change_10 > 0 and p_change_20 >0 and p_change_30 >0 and p_change_60 >0 and p_change_90 >0:
		print(Fore.YELLOW+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	elif p_change > 0:
		print(Fore.RED+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	elif p_change < 0:
		print(Fore.GREEN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	else:
		print(date_now+' '+price_msg+' '+p_change_title+p_change_msg)
