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
import pdb

def get_day(day,loop_i,workday):
	num = day
	my_date_tmp = list()
	for my_day in range(loop_i-1,loop_i-num,-1):
		my_date_tmp.append(str(workday.date[my_day]))
	return(my_date_tmp)

def get_p_change_for_days(date_list,df,day_list):
	my_change_sum = 0.0
	count = 0
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

def get_day_data(p_change_list,day_list):
	day_data = dict()
	for day,data in zip(day_list,p_change_list):
		day_data[day] = data
	return(day_data)

def get_color(text):
	my_number = float(text)
	if my_number > 0:
		my_text = colored(text, 'red')
	elif my_number < 0:
		my_text = colored(text, 'green')
	else:
		my_text = text
	return(my_text)

def get_info(info_para_list):
	df,date_today,workday,day_list,i = info_para_list
	price_open = df[df.index == date_today].open[0] #开盘价格
	price_min = df[df.index == date_today].low[0] #当日最低
	price_max = df[df.index == date_today].high[0] #当日最高
	p_change = df[df.index == date_today].p_change[0] #当日股票涨幅
	p_change_list = get_p_change_for_days(get_day(121,i,workday),df,day_list) #120交易日 取样列表
	day_data = get_day_data(p_change_list,day_list) #股票时间点取值
	price_info_list = [price_open,price_min,price_max,p_change,p_change_list,day_data]
	#print(price_info_list)
	return(price_info_list)

def color4rules(date_today,price_info_list):
	price_open,price_min,price_max,p_change,p_change_list,day_data = price_info_list
	num = len(day_data) +1
	count = 0
	#print(price_open,p_change,day_data)

	if p_change >=0:
		count = count +1
	else:
		count = count -1

	for k,v in day_data.items():
		if v >= 0:
			count =count +1
		else:
			count =count -1
	persent = (num + count) / num * 100 - 100
	persent_str = str(int(persent))

	#if persent <= -80 and price_open <= 15:
	if persent <= -80:
		output_color = 'cyan'
	#elif persent > -80 and persent <= -70 and price_open <= 15:
	elif persent > -80 and persent <= -70:
		output_color = 'magenta'
	#elif persent >= 80 :
	#	output_color = 'yellow'
	#elif p_change > 0:
	#	output_color = 'red'
	#elif p_change < 0:
	#	output_color = 'green'
	else:
		output_color = 'no'
	return(output_color,persent_str)

#def color4output(date_today,stock_basics_list,price_info_list,color,persent):
def color4output(date_today,stock_basics_list,price_info_list,sh_info_list,color,persent,persent_sh):

	stock_code,stock_name,stock_industry,stock_area,stock_pe,stock_pb = stock_basics_list
	price_open,price_min,price_max,p_change,p_change_list,day_data = price_info_list
	sh_open,sh_min,sh_max,sh_p_change,sh_p_change_list,day_data_sh = sh_info_list

	#print(stock_basics_list,sh_info_list)

	price_msg = 'P(min/max):\t'+("%.2f" % price_min)+' '+("%.2f" % price_max)+'\t'+'price:\t'+ ("%.2f" % price_open)
	persent_msg = '\t[股票/大盘](当日/取样)\t'+get_color("%.2f" % p_change)+'\t'+get_color("%.2f" % sh_p_change)+'\t|\t'+get_color(str(int(persent)))+'\t'+get_color(persent_sh)
	#stock_info_msg = '\t市盈率\t'+stock_pe+'\t市净率\t'+stock_pb+'\t行业 '+stock_industry
	stock_info_msg = '\t市盈率\t'+stock_pe+'\t'+stock_industry
	p_change_title = ''
	#persent_msg = ''

	head_msg = stock_code +" "+stock_name+"\t"
	mid_msg = date_today+' '+price_msg+' '+p_change_title
	if color == 'yellow':
		print(head_msg+Fore.YELLOW+mid_msg+Style.RESET_ALL+persent_msg+stock_info_msg)
	elif color == 'cyan':
		print(head_msg+Fore.CYAN+mid_msg+Style.RESET_ALL+persent_msg+stock_info_msg)
	elif color == 'red':
		print(head_msg+Fore.RED+mid_msg+Style.RESET_ALL+persent_msg+stock_info_msg)
	elif color == 'green':
		print(head_msg+Fore.GREEN+mid_msg+Style.RESET_ALL+persent_msg+stock_info_msg)
	elif color == 'magenta':
		print(head_msg+Fore.MAGENTA+mid_msg+Style.RESET_ALL+persent_msg+stock_info_msg)
	else:
		print(head_msg+mid_msg+persent_msg)

def do_it(code,basics):

	stock_name = str(basics[basics.index == code][['name']].values[0][0])
	stock_code = code

	num4days = 200
	now = datetime.date.today()
	yestoday = now - datetime.timedelta(days=1)
	end_day = now - datetime.timedelta(days=num4days)
	workday = pd.bdate_range(start=str(end_day),end=str(yestoday))
	
	try:
		df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
		df_sh = ts.get_hist_data('sh',start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)	
	
	days = len(workday.date)
	
	for i in range(days-1,days-2,-1):
		my_str = ''
		date_today = str(workday.date[i])
		date_yestoday = str(workday.date[i-1])
	
		try:
			price_open = df[df.index == date_today].open[0]
			yestoday_price_open = df[df.index == date_yestoday].open[0]
		except:
			continue
	
		if price_open != price_open:
			continue
	
		info_para_list = [df,date_today,workday,day_list,i]
		price_info_list = get_info(info_para_list) #获取股票信息

		info_para_list = [df_sh,date_today,workday,day_list,i]
		sh_info_list = get_info(info_para_list) 
		#print(sh_info_list)
		#sys.exit()
		color,persent = color4rules(date_today,price_info_list)
		color_sh,persent_sh = color4rules(date_today,sh_info_list)
		#print(color_sh,persent_sh,sh_info_list)
		if color != 'no':
			stock_industry = str(basics[basics.index == code][['industry']].values[0][0]) #行业
			stock_area = str(basics[basics.index == code][['area']].values[0][0]) #区域
			stock_pe = str(basics[basics.index == code][['pe']].values[0][0]) #市盈率
			stock_pb = str(basics[basics.index == code][['pb']].values[0][0]) #市净率

			#stock_basics_list = [stock_code,stock_name,stock_industry,stock_area,stock_pe,stock_pb,stock_eps]
			stock_basics_list = [stock_code,stock_name,stock_industry,stock_area,stock_pe,stock_pb]
			#print(price_info_list,sh_info_list)
			color4output(date_today,stock_basics_list,price_info_list,sh_info_list,color,persent,persent_sh)

if __name__ == "__main__":

	colorama.init()
	day_list = [3,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95,100,105,110,115,120] #取样时间列表
	
	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('timeout!')
		sys.exit(1)
	
	stock_list = stock_basics[stock_basics.pe > 80].index.values

	pool = multiprocessing.Pool(processes=4)
	for stock_code in sorted(stock_list):
		pool.apply_async(do_it, (stock_code,stock_basics))
	pool.close()
	pool.join()
