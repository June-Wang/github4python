#!/usr/bin/env python3.4

import sys
import re
import datetime
import time
import multiprocessing
import tushare as ts
import pandas as pd
import colorama
from colorama import Fore, Back, Style
from termcolor import colored, cprint

#def get_days_persent(df,day_count,days_list_persent):

def get_weight(stock_code,start_day,end_day):
	try:
		df = ts.get_hist_data(stock_code,start=str(start_day),end=str(end_day))
	except:
		print('get_hist_data timeout!')
	
	stock_close = list()
	for workday in df.index.values:
		#print(workday,df[df.index == workday].close[0],stock_code)
		stock_close.append(float(df[df.index == workday].close[0]))

	mark2weight = 0
	status = 'ok'
	items = [i for i in range(0,5)]
	for i in range(0,5):
		day_count_list = list(map(lambda x:x+i,items))
		close_list = list()
		for x in day_count_list:
			try:
				close_list.append(stock_close[x])
			except:
				status = 'timeout'
				break
		#print(str(stock_close[i]),close_list)
		if status == 'timeout':
			break
		if stock_close[i] == min(close_list):
			mark2weight += 1
	return(mark2weight)

if __name__ == "__main__":
	colorama.init()

	num4days = 6
	day_list = [i for i in range(5,185,5)]
	day_list.append(3)

	now = datetime.date.today()
	d = datetime.datetime.now()
	d = d.replace(hour = 15,minute = 00,second = 0)

	if datetime.datetime.now() > d:
		end_day = now
	else:
		end_day = now - datetime.timedelta(days=1)

	start_day = now - datetime.timedelta(days=num4days*2)

	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('get_stock_basics timeout!')
		sys.exit(1)

	#stock_list = stock_basics.index.values
	stock_list = ['002113','000998','600519','600188']

	down2list = list()
	#pool = multiprocessing.Pool(processes=4)
	for stock_code in sorted(stock_list):
		#print('code:'+stock_code)
		mark2weight = get_weight(stock_code,start_day,end_day)
		#print(stock_code,str(mark2weight))
		if mark2weight >=3:
			#print(stock_code)
			down2list.append(stock_code)	
		#sys.exit(1)
	#print(down2list)

	num4days = 300
	start_day = now - datetime.timedelta(days=num4days+max(day_list)+100)
	try:
		df = ts.get_hist_data(code,start=str(start_day),end=str(end_day))
	except:
		print('get_hist_data timeout!')
		sys.exit(1)
	for stock_code in down2list:
		
