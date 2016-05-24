#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd
import colorama
from colorama import Fore, Back, Style
from termcolor import colored, cprint
import time

colorama.init()

try:
	basics = ts.get_stock_basics()
except:
	print('timeout!')
	sys.exit(1)

stock_list = basics[basics.pe >80].index.values
#stock_list = basics[basics.pe >250][basics.esp > 0].index.values
#stock_list = basics[basics.pe >250][basics.esp > 0].index.copy()
for code in stock_list:
	#stock_name = str(stock_list[stock_list.index == code].values[0][0])
	stock_name = str(basics[basics.index == code][['name']].values[0][0])
	stock_code = code
	num4days = 1
	now = datetime.date.today()
	yestoday = now - datetime.timedelta(days=1)
	end_day = now - datetime.timedelta(days=num4days+121)
	workday = pd.bdate_range(start=str(end_day),end=str(yestoday))
	
	try:
		df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)	
	
	days = len(workday.date)
	
	def get_day(day,loop_i):
		global workday
		#num = day+1
		num = day
		my_date_tmp = list()
		for my_day in range(loop_i-1,loop_i-num,-1):
			my_date_tmp.append(str(workday.date[my_day]))
		return(my_date_tmp)
	
	def get_p_change_for_days(date_list):
		global df
		my_change_sum = 0.0
		count = 0
		day_list = [3,5,10,15,20,30,60,90,120]
		data_list = list()
		for my_date in date_list:
			try:
				my_change_tmp = float(df[df.index == my_date].p_change[0])
			except:
				my_change_tmp = 0.0
			my_change_sum += my_change_tmp
			count = count +1
			if count in day_list:
				#print(count)
				data_list.append(my_change_sum)
		return(data_list)
	
	def get_color(text):
		my_number = float(text)
		if my_number > 0:
			my_text = colored(text, 'red')
		elif my_number < 0:
			my_text = colored(text, 'green')
		else:
			my_text = text
		return(my_text)
	
	#mt_str = 'hello'
	#print(get_color(mt_str))
	#sys.exit(1)	
				
	for i in range(days-1,days-2,-1):
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
	
		p_change_list = get_p_change_for_days(get_day(121,i))
		#print(p_change_list)
		#sys.exit()
	
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
		
		#price_msg = 'price(close/min/max): '+("%.2f" % price_close)+' '+("%.2f" % price_min)+' '+("%.2f" % price_max)
		price_msg = 'P(min/max):\t'+("%.2f" % price_min)+' '+("%.2f" % price_max)
		
		p_change_title = 'C(1/3/5/10/15/20/30/60/90/120):\t'
		p_change_msg = get_color(("%.2f" % p_change))
		for p_change_value in p_change_list:
			p_change_msg += '\t'+ get_color(("%.2f" % p_change_value))
		
		day_data = dict()
		day_list = [3,5,10,15,20,30,60,90,120]
		#print(list(zip(day_list,p_change_list)))
		#sys.exit(0)
		for day,data in zip(day_list,p_change_list):
			day_data[day] = data
		if price_open <= 15 and p_change < 0 and day_data[3] < 0 and day_data[5] <0 and day_data[10] < 0 and day_data[15] < 0  and day_data[20] < 0 and day_data[30] < 0 and day_data[60] < 0 and day_data[90] < 0 and day_data[120] < 0:
			print(stock_code +" "+stock_name+"\t"+Fore.CYAN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
			#time.sleep(2)
	#	elif p_change < 0 and day_data[3] > 0 and day_data[5] >0 and day_data[10] >0 and day_data[20] >0 and day_data[30] >0 and day_data[60] >0:
	#		print(Fore.YELLOW+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	#	elif p_change > 0:
	#		print(Fore.RED+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	#	elif p_change < 0:
	#		print(Fore.GREEN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	#	else:
	#		print(date_now+' '+price_msg+' '+p_change_title+p_change_msg)

