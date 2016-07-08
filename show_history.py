#!/usr/bin/env python3.4

import sys
import datetime
import time
import multiprocessing
import pandas as pd
import requests
import tushare as ts
import colorama
from colorama import Fore, Back, Style
from termcolor import colored, cprint

def get_color(text):
	my_number = float(text)
	if my_number > 0:
		my_text = colored(text, 'red')
	elif my_number < 0:
		my_text = colored(text, 'green')
	else:
		my_text = text
	return(my_text)

def get_price_info(code,df,day_count):
	date = df.index.values[day_count]
	price = {}
	price_open = df[df.index == date].open[0] #开盘价格
	price_close = df[df.index == date].close[0] #收盘价格
	price_min = df[df.index == date].low[0] #当日最低
	price_max = df[df.index == date].high[0] #当日最高
	p_change = df[df.index == date].p_change[0] #当日股票涨幅
	price[code] = {'open':price_open,'close':price_close,
					'min':price_min,'max':price_max,
					'p_change':p_change}
	return(price[code])

def get_days_persent(df,day_count,days_list_persent):
	days_list = days_list_persent
	down_persent = {}
	up_persent = {}
	max_persent = {}
	min_persent = {}
	data_day = list()
	for i in range(max(days_list)+1):
		date_i = df.index.values[day_count+i]
		data_day.append(float(df[df.index == date_i].close[0]))
		#print(data_day)
		if i in days_list:
			down_persent[i]=(data_day[0] - data_day[-1])/max(data_day) *100
			up_persent[i]=(data_day[0] - data_day[-1])/min(data_day) *100

			max_persent[i]=(data_day[0] - max(data_day))/max(data_day) *100
			min_persent[i]=(data_day[0] - min(data_day))/min(data_day) *100

	down_count = 0
	up_count = 0
	min_count = 0
	max_count = 0
	day_sum = len(days_list_persent)
	for i in days_list_persent:
		if down_persent[i] < 0:
			down_count +=1
		else:
			down_count -=1

		if up_persent[i] < 0:
			up_count +=1
		else:
			up_count -=1

		if max_persent[i] == 0:
			max_count +=1
		else:
			max_count -=1

		if min_persent[i] == 0:
			min_count +=1
		else:
			min_count -=1

	return(int(down_count/day_sum),int(up_count/day_sum),\
		int(min_count/day_sum),int(max_count/day_sum))

def get_data_list(df,day_list,day_count):
	change_sum = 0.0
	count = 0
	data_list = {}
	end_num = day_list[-1]+1
	for date in df.index.values[day_count:]:
		if count < end_num:
			try:
				my_change_tmp = float(df[df.index == date].p_change[0])
			except:
				my_change_tmp = 0.0
			change_sum += my_change_tmp
			count = count +1
			if count in day_list:
				data_list[count] = change_sum
		else:
			break
	#print(len(data_list))
	return(data_list,len(data_list))

def rules(df,day_list,data_list_dict,p_change):
	num = len(day_list) +1
	count = 0

	if p_change >=0:
		count = count +1
	else:
		count = count -1

	for day in day_list:
		try:
			if  data_list_dict[day] >= 0:
				count =count +1
			else:
				count =count -1
		except:
			break	
	persent =  count / num * 100
	return(persent)

def color(color,mid_msg,end_msg):
	if color == 'yellow':
		print(Fore.YELLOW+mid_msg+Style.RESET_ALL+'\t'+end_msg)
	elif color == 'cyan':
		print(Fore.CYAN+mid_msg+Style.RESET_ALL+'\t'+end_msg)
	elif color == 'magenta':
		print(Fore.MAGENTA+mid_msg+Style.RESET_ALL+'\t'+end_msg)
	elif color == 'red':
		print(Fore.RED+mid_msg+Style.RESET_ALL+'\t'+end_msg)
	elif color == 'green':
		print(Fore.GREEN+mid_msg+Style.RESET_ALL+'\t'+end_msg)

def get_share(stock_code):

	url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	try:
		table = pd.read_html(resp.text)[0]
	except:
		print('获取配股分红信息失败！')
		year_list = list()
		return(year_list)
	year_list = [ str(year[0]) for year in table[['除权除息日']].values]
	return(year_list)

def color4msg(df,code,day_count,price_dict,sh_price_dict,\
persent,sh_persent,count_list,days_list_persent,year_list):
	
	date = df.index.values[day_count]
	down_count,up_count,min_count,max_count = count_list
	#print(str(date),year_list)
	if str(date) in year_list:
		share_msg = '配股分红'
	else:
		share_msg = ''
	head_msg = date + '\t'+'min/max/close'
	mid_msg = head_msg+'\t'+("%.2f" % price_dict[code]['min'])+'\t'+("%.2f" % price_dict[code]['max'])+'\t'+("%.2f" % price_dict[code]['close'])
	persent_msg = get_color(("%.2f" % persent))+'\t'+get_color(("%.2f" % sh_persent))+'\t'+str(int(sh_price_dict['close']))
	p_change_msg = get_color("%.2f" % price_dict[code]['p_change'])+'\t'+\
		get_color("%.2f" % sh_price_dict['p_change'])
	du_msg = 'down/up'+'\t'+get_color(str(down_count))+'\t'+get_color(str(up_count))
	mm_msg = 'min/max'+'\t'+get_color(str(min_count))+'\t'+get_color(str(max_count))
	end_msg = persent_msg+'\t'+p_change_msg+'\t'+du_msg+'\t'+mm_msg+'\t'+share_msg

	#day_sum = len(days_list_persent)
	
	#if #persent <=-85 and sh_persent <=0 and down_count == 1 and up_count == 1 and min_count ==1: # or \
	if	(down_count == 1 and up_count == 1 and min_count ==1 and \
		persent <=0 and sh_persent <=0 and \
		(price_dict[code]['p_change'] <=0 and price_dict[code]['p_change'] >-9) and \
		(sh_price_dict['p_change'] <=0 or sh_price_dict['p_change'] >0)):
		
		color('cyan',mid_msg,end_msg)
	elif down_count == -1 and up_count == -1 and max_count ==1 and \
		persent >0 and \
		price_dict[code]['p_change'] >0 and sh_price_dict['p_change']>0:

		color('yellow',mid_msg,end_msg)
	elif price_dict[code]['p_change'] > 0:
		color('red',mid_msg,end_msg)
	elif price_dict[code]['p_change'] < 0:
		color('green',mid_msg,end_msg)

def do_it(code,basics,yestoday,end_day,day_list):

	try:
		df = ts.get_hist_data(code,start=str(end_day),end=str(yestoday))
		df_sh = ts.get_hist_data('sh',start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)

	price_dict = {}
	sh_price_dict = {}
	day_count = 0
	p_change_sum = 0
	sh_p_change_sum = 0
	count_list = list()
	year_list = get_share(code) 

	days_list_persent = [3,5,10]
	for day in df.index.values:
		try:
			price_dict[code] = get_price_info(code,df,day_count)
			#down_count,up_count,max_count,min_count = get_days_persent(df,day_count,days_list_persent)
			count_list = get_days_persent(df,day_count,days_list_persent)
			#print(count_list)
			data_list_dict,num25 = get_data_list(df,day_list,day_count)
			#print(num25)
			if num25 <25:
				break
			p_change = price_dict[code]['p_change']
			persent = rules(df,day_list,data_list_dict,p_change)

			sh_price_dict = get_price_info('sh',df_sh,day_count)
			sh_data_list_dict,num25 = get_data_list(df_sh,day_list,day_count)
			sh_p_change = sh_price_dict['p_change']
			sh_persent = rules(df_sh,day_list,sh_data_list_dict,sh_p_change)
			if p_change >=0:
				p_change_sum +=1
			else:
				p_change_sum -=1
			if sh_p_change >=0:
				sh_p_change_sum +=1
			else:
				sh_p_change_sum -=1
		except:
			break
		color4msg(df,code,day_count,price_dict,sh_price_dict,\
			persent,sh_persent,count_list,days_list_persent,year_list)
		day_count +=1
		#print(day_count)
	print('code:\t'+get_color(str(p_change_sum))+'\t'+'sh:\t'+get_color(str(sh_p_change_sum)))

if __name__ == "__main__":

	colorama.init()
	stock_code = sys.argv[1]
	num4days = 300

	day_list = [i for i in range(5,185,5)]
	day_list.append(3)

	now = datetime.date.today()
	d = datetime.datetime.now()
	d = d.replace(hour = 15,minute = 00,second = 0)

	if datetime.datetime.now() > d:
		yestoday = now
	else:
		yestoday = now - datetime.timedelta(days=1)

	end_day = now - datetime.timedelta(days=num4days+max(day_list)+100)

	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('timeout!')
		sys.exit(1)

	do_it(stock_code,stock_basics,yestoday,end_day,sorted(day_list))
