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

def get_weight(df):
	stock_close = list()
	try:
		for workday in df.index:
		#print(workday,df[df.index == workday].close[0],stock_code)
			stock_close.append(float(df[df.index == workday].close[0]))
	except:
		mark2weight=0
		return(mark2weight)

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

def get_data_list(df,day_list):
	change_sum = 0.0
	count = 0
	data_list = {}
	#for my_date in date_list:
	for date in df.index.values:
		try:
			change_tmp = float(df[df.index == date].p_change[0])
		except:
			change_tmp = 0.0
		change_sum += change_tmp
		count = count +1
		#if count in day_list:
		data_list[count] = change_sum
	return(data_list)

def rules(day_list,data_list_dict,p_change):
	num = len(day_list) +1
	count = 0

	if p_change >=0:
		count = count +1
	else:
		count = count -1

	for day in day_list:
		if  data_list_dict[day] >= 0:
			count =count +1
		else:
			count =count -1
	persent =  count / num * 100
	return(persent)

def get_price_info(code,df):
	date = df.index.values[0]
	price = {}
	price_open = df[df.index == date].open[0] #开盘价格
	price_close = df[df.index == date].close[0] #开盘价格
	price_min = df[df.index == date].low[0] #当日最低
	price_max = df[df.index == date].high[0] #当日最高
	p_change = df[df.index == date].p_change[0] #当日股票涨幅
	price[code] = {'open':price_open,'close':price_close,'min':price_min,'max':price_max,'p_change':p_change}
	return(price[code])

def get_w_data(data_list_dict,days):

	w_data_list = [data_list_dict[i] for i in range(1,days)]

	#print(w_data_list)
	up_data = 0
	down_data = 0
	for data in w_data_list:
		if data >= 0:
			up_data += 1
		else:
			down_data +=1

	w_data = (up_data-down_data)/len(w_data_list)*100
	return(w_data)

def do_it(stock_code,start_day,end_day,day_list,stock_basics):
	#print(stock_code,start_day,end_day)
	try:
		df_hist_data = ts.get_hist_data(stock_code,start=str(start_day),end=str(end_day))		
	except:
		print('get_hist_data timeout!')
		sys.exit(1)

	lastday = df_hist_data.index.values[0]
	price_dict = {}
	price_dict[stock_code] = get_price_info(stock_code,df_hist_data)

	data_list_dict = get_data_list(df_hist_data,day_list)

	w_data_day_list = [60,90,120]
	w_data_list = [ get_w_data(data_list_dict,i) for i in w_data_day_list ]
	w_data = w_data_list[0] #60
	w_data_avg = sum(w_data_list)/len(w_data_list)

	if w_data <= -90 and w_data_avg <= -90:
		p_change = price_dict[stock_code]['p_change']
		persent = rules(day_list,data_list_dict,p_change)
	
		if persent <= -80 or data_list_dict[10] <= -10:	
			date = str(end_day)[:10]
			name = stock_basics[stock_basics.index == stock_code][['name']].values[0][0]
			industry = stock_basics[stock_basics.index == stock_code][['industry']].values[0][0]
			close = ("%.2f" % price_dict[stock_code]['close'])
			output_args = [date,stock_code,close,'day10:',str(int(data_list_dict[10])),\
					'now/60/avg:',str(int((persent))),str(int(w_data)),str(int(w_data_avg)),name,industry]
			msg = '\t'.join(output_args)
			print(msg)

def job2weight(stock_code,end_day,stock_basics):
	num4days = 60
	day_list = [i for i in range(5,180,5)]
	start_day = now - datetime.timedelta(days=num4days+max(day_list)+61)
	do_it(stock_code,start_day,end_day,day_list,stock_basics)

if __name__ == "__main__":
	colorama.init()
		

	now = datetime.date.today()
	d = datetime.datetime.now()
	d = d.replace(hour = 15,minute = 00,second = 0)

	if datetime.datetime.now() > d:
		end_day = now
	else:
		end_day = now - datetime.timedelta(days=1)

	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('get_stock_basics timeout!')
		sys.exit(1)

	try:
		list_code = sys.argv[1]
		
		if int(list_code) == 500:
			try:
				stock_500 = ts.get_zz500s()
			except:
				print('get_zz500s timeout!')
				sys.exit(1)
			stock_list = stock_500.code.values
		else:
			sys.exit(1)
	except:
		stock_list = stock_basics.index.values

	#stock_list = ['002113','000998','600519','600188']
	pool = multiprocessing.Pool(processes=4)
	for stock_code in sorted(stock_list):
		pool.apply_async(job2weight,(stock_code,end_day,stock_basics))
	pool.close()
	pool.join()
