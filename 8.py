#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd
import colorama
from colorama import Fore, Back, Style
from termcolor import colored, cprint
import time
import multiprocessing

def get_basics_info(code,basics):
	stock_basics = {}
	name = str(basics[basics.index == code][['name']].values[0][0])
	industry = str(basics[basics.index == code][['industry']].values[0][0]) #行业
	area = str(basics[basics.index == code][['area']].values[0][0]) #区域
	pe = str(basics[basics.index == code][['pe']].values[0][0]) #市盈率
	pb = str(basics[basics.index == code][['pb']].values[0][0]) #市净率
	stock_basics[code] = {'name':name,'industry':industry,'area':area,'pe':pe,'pb':pb}
	return(stock_basics[code])

def do_it(code,basics):

	count = 0
	num4days = 200
	now = datetime.date.today()
	yestoday = now - datetime.timedelta(days=1)
	end_day = now - datetime.timedelta(days=num4days)
	#workday = pd.bdate_range(start=str(end_day),end=str(yestoday))

	stock_basics_dict = {}
	stock_basics_dict[code] = get_basics_info(code,basics)
	print(p_change,code,stock_basics_dict[code])

	try:
		df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)

	#days = len(workday.date)

	for date_today in df.index.values:
		date_yestoday=str(datetime.datetime.strptime(date_today, '%Y-%m-%d') + datetime.timedelta(days = -1))[:10]
		print(date_today,date_yestoday)
		try:
			p_change = df[df.index == date_today].p_change[0]
		except:
			continue

		if p_change != p_change:
			continue
		
		sys.exit()
		#count +=1
		#if p_change >3:
		#	num

if __name__ == "__main__":

	colorama.init()

	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('timeout!')
		sys.exit(1)

	stock_list = stock_basics.index.values

	pool = multiprocessing.Pool(processes=4)
	for stock_code in sorted(stock_list):
		pool.apply_async(do_it, (stock_code,stock_basics))
	pool.close()
	pool.join()
