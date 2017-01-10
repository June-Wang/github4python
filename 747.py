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

	start_day = now - datetime.timedelta(days=num4days+10)

	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('get_stock_basics timeout!')
		sys.exit(1)

	stock_list = stock_basics.index.values

	for stock_code in sorted(stock_list):
		try:
			df = ts.get_hist_data(stock_code,start=str(start_day),end=str(end_day))
		except:
			print('get_hist_data timeout!')
		
		stock_close = list()
		for workday in df.index.values:
			print(workday,df[df.index == workday].close[0],stock_code)
			stock_close.append(float(df[df.index == workday].close[0]))
		#print(stock_close)
		#for i in range(5):
		#	for y in range(i+1,i+5):
		#		print(str(i),str(y))
		items = [1,2,3,4,5]
		for i in range(0,5):
			day_count_list = list(map(lambda x:x+i,items))
			for x in day_count_list:
				close_list.append(stock_close[x])
			
			print(close_list)
		sys.exit(1)
