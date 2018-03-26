#!/usr/bin/env python3

import sys
import re
import os
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

def get_data_grow_list(df,day_list):
	count = 0
	w_count = 0
	data_grow_list = {}
	end_num = day_list[-1]+1
	for date in df.index.values:
		if count < end_num:
			try:
				change = float(df[df.index == date].p_change[0])
			except:
				change = 0
			if change >= 0:
				w_count = w_count +1
			else:
				w_count = w_count -1
			count = count +1
			persent = w_count / count * 100
			data_grow_list[count] = persent
		else:
			break
	#print(data_grow_list)
	return(data_grow_list)

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
	data_grow_dict = get_data_grow_list(df_hist_data,day_list)

	p_change = price_dict[stock_code]['p_change']
	persent = rules(day_list,data_list_dict,p_change)

	w_data_list = [ get_w_data(data_list_dict,i) for i in day_list ]
	data_grow_dict = get_data_grow_list(df_hist_data,day_list)
	#print(data_grow_dict)

	w_data_grow_list = [ get_w_data(data_grow_dict,i) for i in day_list ]
	#print(stock_code,w_data_grow_list)

	w_weight_list = [ sum(w_data_list)/len(w_data_list),sum(w_data_grow_list)/len(w_data_grow_list),persent ]
	w_weight = sum(w_weight_list)/len(w_weight_list)
	w_weight_msg = 'W:\t'+str(int(w_weight))

	#print(w_weight_msg)
	if w_weight <= -80:
	#if w_weight <= -80 and persent <= -90 and sh_persent <= 0:
	#if w_weight == -100 and persent == -100:
		date = str(end_day)[:10]
		name = stock_basics[stock_basics.index == stock_code][['name']].values[0][0]
		industry = stock_basics[stock_basics.index == stock_code][['industry']].values[0][0]
		close = ("%.2f" % price_dict[stock_code]['close'])
		output_args = [date,stock_code,close,w_weight_msg,name,industry]
		msg = '\t'.join(output_args)
		print(msg)

def job2weight(stock_code,end_day,stock_basics):
	num4days = 60
	day_list = [i for i in range(5,60)]
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

	file = sys.argv[1]
	if not os.path.isfile(file):
			print(file,'not found!')
			sys.exit(1)

	with open(file,"r") as fh:
			rows = fh.readlines()

	stock_list = list()
	for code in rows:
			m = re.match("^\d{6}$",code)
			if not m:
					continue
			stock_code = code.replace("\n", "")
			stock_list.append(stock_code)

	pool = multiprocessing.Pool(processes=4)
	for stock_code in sorted(stock_list):
		pool.apply_async(job2weight,(stock_code,end_day,stock_basics))
	pool.close()
	pool.join()
