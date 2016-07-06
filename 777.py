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

def get_color(text):
	my_number = float(text)
	if my_number > 0:
		my_text = colored(text, 'red')
	elif my_number < 0:
		my_text = colored(text, 'green')
	else:
		my_text = text
	return(my_text)

def get_basics_info(code,basics):
	stock_basics = {}
	name = str(basics[basics.index == code][['name']].values[0][0])
	industry = str(basics[basics.index == code][['industry']].values[0][0]) #行业
	area = str(basics[basics.index == code][['area']].values[0][0]) #区域
	pe = str(basics[basics.index == code][['pe']].values[0][0]) #市盈率
	try:
		pb = str(basics[basics.index == code][['pb']].values[0][0]) #市净率
	except:
		pb = 0.0
	stock_basics[code] = {'name':name,'industry':industry,'area':area,'pe':pe,'pb':pb}
	return(stock_basics[code])

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

def get_data_list(df,day_list):
	change_sum = 0.0
	count = 0
	data_list = {}
	#for my_date in date_list:
	for date in df.index.values:
		try:
			my_change_tmp = float(df[df.index == date].p_change[0])
		except:
			my_change_tmp = 0.0
		change_sum += my_change_tmp
		count = count +1
		if count in day_list:
			data_list[count] = change_sum
	return(data_list)

def get_days_persent(df,day_count,days_list_persent):
	days_list = days_list_persent
	down_persent = {}
	up_persent = {}
	data_day = list()
	for i in range(max(days_list)+1):
		date_i = df.index.values[day_count+i]
		data_day.append(float(df[df.index == date_i].close[0]))
		#print(data_day)
		if i in days_list:
			down_persent[i]=(data_day[0] - max(data_day))/max(data_day) *100
			up_persent[i]=(data_day[0] - min(data_day))/min(data_day) *100
	return(down_persent,up_persent)

def rules(df,day_list,data_list_dict,p_change):
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

def color4msg(code,yestoday,stock_basics_dict,price_dict,persent,sh_persent,down_persent,up_persent,days_list_persent):
	date = str(yestoday)[:10]
	head_msg = code+'\t'+stock_basics_dict[code]['name']
	mid_msg = date + '\t'+'P(min/max/close):\t'+("%.2f" % price_dict[code]['min'])+'\t'+("%.2f" % price_dict[code]['max'])+'\t'+("%.2f" % price_dict[code]['close'])
	end_msg = get_color(("%.2f" % persent))+'\t'+get_color(("%.2f" % sh_persent))+'\t市盈率\t'+stock_basics_dict[code]['pe']+'\t'+stock_basics_dict[code]['industry']

	down_sum = 0.0
	up_sum = 0.0
	for i in days_list_persent:
		down_sum += down_persent[i]
		up_sum += up_persent[i]

	if persent <0 and sh_persent <=0 and price_dict[code]['p_change'] > -9 and \
		price_dict[code]['p_change'] <=0 and sh_price_dict['p_change']<=0 and \
		down_persent[3]<0 and down_persent[5]<0 and down_persent[10]<0 and \
		up_sum ==0:
		print(Fore.CYAN+mid_msg+Style.RESET_ALL+'\t'+head_msg +'\t'+end_msg)
	#elif persent <0 and price_dict[code]['p_change'] > -9 and \
    #    price_dict[code]['p_change'] <=0 and \
    #    down_persent[3]<0 and down_persent[5]<0 and down_persent[10]<0 and \
    #    up_sum == 0:
	#	print(Fore.MAGENTA+mid_msg+Style.RESET_ALL+'\t'+head_msg +'\t'+end_msg)
	#elif persent > -80 and persent <= -70:
	#	print(Fore.MAGENTA+mid_msg+Style.RESET_ALL+'\t'+head_msg +'\t'+end_msg)

def do_it(code,basics,yestoday,end_day,day_list,sh_persent):

	stock_basics_dict = {}
	stock_basics_dict[code] = get_basics_info(code,basics)

	try:
		df = ts.get_hist_data(code,start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)

	#前一天股票价格信息
	price_dict = {}
	price_dict[code] = get_price_info(code,df)
	
	days_list_persent = [3,5,10]
	day_count = 0
	down_persent,up_persent = get_days_persent(df,day_count,days_list_persent)

	data_list_dict = get_data_list(df,day_list)
	p_change = price_dict[code]['p_change']
	persent = rules(df,day_list,data_list_dict,p_change)

	#color4msg(code,yestoday,stock_basics_dict,price_dict,persent,sh_persent)
	color4msg(code,yestoday,stock_basics_dict,price_dict,persent,sh_persent,down_persent,up_persent,days_list_persent)

if __name__ == "__main__":

	colorama.init()

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

	try:
		df_sh = ts.get_hist_data('sh',start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)

	sh_price_dict = {}
	sh_price_dict = get_price_info('sh',df_sh)
	sh_data_list_dict = get_data_list(df_sh,day_list)
	sh_p_change = sh_price_dict['p_change']
	sh_persent = rules(df_sh,day_list,sh_data_list_dict,sh_p_change)

	stock_list = stock_basics.index.values
		
	pool = multiprocessing.Pool(processes=4)
	for stock_code in sorted(stock_list):
		pool.apply_async(do_it, (stock_code,stock_basics,yestoday,end_day,sorted(day_list),sh_persent))
	pool.close()
	pool.join()