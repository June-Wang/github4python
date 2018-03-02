#!/usr/bin/env python3.4

import sys
import re
import os
import datetime
import time
import multiprocessing
import tushare as ts
import pandas as pd
#import colorama
#from colorama import Fore, Back, Style
#from termcolor import colored, cprint

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

#def get_price_info(code,df):
#	date = df.index.values[0]
#	price = {}
#	price_open = df[df.index == date].open[0] #开盘价格
#	price_close = df[df.index == date].close[0] #开盘价格
#	price_min = df[df.index == date].low[0] #当日最低
#	price_max = df[df.index == date].high[0] #当日最高
#	p_change = df[df.index == date].p_change[0] #当日股票涨幅
#	price[code] = {'open':price_open,'close':price_close,'min':price_min,'max':price_max,'p_change':p_change}
#	return(price[code])

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

	#lastday = df_hist_data.index.values[0]
	price_dict = {}
	price_dict[stock_code] = get_price_info(stock_code,df_hist_data)
	p_change = price_dict[stock_code]['p_change']

	persent = rules(day_list,data_list_dict,p_change)

	data_list_dict = get_data_list(df_hist_data,day_list)
	w_data_list = [ get_w_data(data_list_dict,i) for i in day_list ]
	data_grow_dict = get_data_grow_list(df_hist_data,day_list)
	#print(data_grow_dict)

	w_data_grow_list = [ get_w_data(data_grow_dict,i) for i in day_list ]
	#print(stock_code,w_data_grow_list)

	w_weight_list = [ sum(w_data_list)/len(w_data_list),sum(w_data_grow_list)/len(w_data_grow_list),persent ]
	w_weight = sum(w_weight_list)/len(w_weight_list)
	#w_weight_msg = 'W:\t'+str(int(w_weight))
	w_weight_msg = str(int(w_weight))

	#print(w_weight_msg)
	#if w_weight <= -80 and persent <= 90 and sh_persent <= 0:
	#if w_weight == -100:
	date = str(end_day)[:10]
	name = stock_basics[stock_basics.index == stock_code][['name']].values[0][0]
	industry = stock_basics[stock_basics.index == stock_code][['industry']].values[0][0]
	close = ("%.2f" % price_dict[stock_code]['close'])
	output_args = [date,stock_code,name,close,w_weight_msg,industry]
	#msg = '\t'.join(output_args)
	#print(msg)
	return(output_args)

#def job2weight(stock_code,end_day,stock_basics):
#	num4days = 30
#	day_list = [i for i in range(5,num4days)]
#	start_day = now - datetime.timedelta(days=num4days+max(day_list))
#	result = do_it(stock_code,start_day,end_day,day_list,stock_basics)
#	return(result)

def color_negative_red(val):
	"""
	Takes a scalar and returns a string with
	the css property `'color: red'` for negative
	strings, black otherwise.
	"""
	color = 'red' if val < 0 else 'black'
	return 'color: %s' % color

def get_day_persent(data_list_dict):
    up2days = 0
    count = 0
    for num in data_list_dict:
        if data_list_dict[num] > 0:
            up2days +=1
        count +=1

    up2persents = float(up2days)/float(len(data_list_dict)) * 100
    down2persents = (100 - up2persents) * -1
    day_persents = int(up2persents + down2persents)
    #print(str(up2days),str(count))
    return(day_persents)

def get_end_day(now):
	"""
	获取工作日的最后一天
	"""
	d = datetime.datetime.now()
	d = d.replace(hour = 15,minute = 00,second = 0)

	if datetime.datetime.now() > d:
		end_day = now
	else:
		end_day = now - datetime.timedelta(days=1)
	return(end_day)

def get_start_day(now,num4days,day_list):
	"""
	获取时间周期的开始时间
	"""
	#day_list = [i for i in range(5,num4days)]
	start_day = now - datetime.timedelta(days=num4days+max(day_list))
	return(start_day)

def get_df_hist_data(stock_code,start_day,end_day):
    """
    获取股票的历史数据，参数：股票代码(stock_code)、时间周期(num4days)
	开始时间(start_day)、结束时间(end_day)
    """
    try:
        df_hist_data = ts.get_hist_data(stock_code,start=str(start_day),end=str(end_day))
    except:
        print('get_hist_data timeout!')
        sys.exit(1)
    return(df_hist_data)

def get_stock_info(stock_code,stock_basics,df_hist_data,end_day):
	date = str(end_day)[:10]
	name = stock_basics[stock_basics.index == stock_code][['name']].values[0][0]
	industry = stock_basics[stock_basics.index == stock_code][['industry']].values[0][0]
	#close = ("%.2f" % price_dict[stock_code]['close'])
	lastday = df_hist_data.index.values[0]
	close = ("%.2f" % df_hist_data[df_hist_data.index == lastday].close[0])
	output_args = [date,stock_code,name,close,industry]
	#msg = '\t'.join(output_args)
	#print(msg)
	return(output_args)

def get_stock_basics():
	"""
	获取所有股票的基本信息
	"""
	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('get_stock_basics timeout!')
		sys.exit(1)
	return(stock_basics)

def job2weight(stock_code,start_day,end_day,stock_basics):
	#Beginning
	#stock_code='000998'
	df_hist_data = get_df_hist_data(stock_code,start_day,end_day)

	data_list_dict = get_data_list(df_hist_data,day_list)
	
	#rules
	#date = df_hist_data.index.values[0]
	#p_change = df_hist_data[df_hist_data.index == date].p_change[0]
	#persent = rules(day_list,data_list_dict,p_change)

	#get_day_persent
	persent = get_day_persent(data_list_dict)

	#print(persent)

	w_data_list = [ get_w_data(data_list_dict,i) for i in day_list ]

	data_grow_dict = get_data_grow_list(df_hist_data,day_list)	
	w_data_grow_list = [ get_w_data(data_grow_dict,i) for i in day_list ]

	w_weight_list = [ sum(w_data_list)/len(w_data_list),sum(w_data_grow_list)/len(w_data_grow_list),persent ]
	w_weight = sum(w_weight_list)/len(w_weight_list)
	#print(str(w_weight))


	stock_info = get_stock_info(stock_code,stock_basics,df_hist_data,end_day)
	stock_info.append(str(int(w_weight)))
	#print(stock_info)
	#sys.exit(1)
	#end
	return(stock_info)

if __name__ == "__main__":

	num4days=30
	day_list = [i for i in range(5,num4days)]

	now = datetime.date.today()
	end_day = get_end_day(now)
	start_day = get_start_day(now,num4days,day_list)

	stock_basics=get_stock_basics()

	cpus = multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=cpus)

	stock_list = ['000998','600188','601933']
	results = []
	for stock_code in sorted(stock_list):
		result = pool.apply_async(job2weight,(stock_code,start_day,end_day,stock_basics))
		results.append(result.get())
		#print(result.get())
	pool.close()
	pool.join()

	#print(results)
	df_html = pd.DataFrame(results,columns=['日期','代码','名称','价格','行业','权重'])
	print(df_html.to_html(index=False))
