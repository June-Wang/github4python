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
			#if count in day_list:
			data_list[count] = change_sum
		else:
			break
	return(data_list,len(data_list))

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

def do_it(code,start_day,end_day,day_list):

	try:
		df = ts.get_hist_data(code,start=str(start_day),end=str(end_day))
		df_sh = ts.get_hist_data('sh',start=str(start_day),end=str(end_day))
	except:
		print('get_hist_data timeout!')
		sys.exit(1)

	price_dict = {}
	sh_price_dict = {}
	day_count = 0
	p_change_sum = 0
	sh_p_change_sum = 0
	year_list = get_share(code) 
	now_price = 0.0

	price_list = list()

	act_list = list()
	act_buy_list = list()
	act_sell_list = list()

	days_list_persent = [3,5,10]
	for_end = yestoday - datetime.timedelta(days=360)
	for day in df.index.values:
		today = datetime.datetime.strptime(day, "%Y-%m-%d").date()
		if (yestoday - today).days > 430:
			continue
		try:
			price_dict[code] = get_price_info(code,df,day_count)
			data_list_dict,num25 = get_data_list(df,day_list,day_count)

			if num25 <25:
				break
			p_change = price_dict[code]['p_change']

			sh_price_dict = get_price_info('sh',df_sh,day_count)
			sh_p_change = sh_price_dict['p_change']
			sh_data_list_dict,num25 = get_data_list(df_sh,day_list,day_count)

		except:
			break

		if day_count == 0:
			now_price = price_dict[code]['close']

		date = df.index.values[day_count]

		if str(date) in year_list:
			share_msg = '配股分红'
		else:
			share_msg = ''
	
		persent = get_day_persent(data_list_dict)	
		sh_persent = get_day_persent(sh_data_list_dict)

		#down2persent = max([ data_list_dict[i] for i in days_list_persent ])
		#up2persent = min([ data_list_dict[i] for i in days_list_persent ])
		
		head_msg = date + '\t'+'min/max/close'
		mid_msg = head_msg+'\t'+("%.2f" % price_dict[code]['min'])+'\t'+("%.2f" % price_dict[code]['max'])+'\t'+("%.2f" % price_dict[code]['close'])
		persent_msg = get_color(str(int(persent)))+'\t'+get_color(str(int(sh_persent)))+'\t'+str(int(sh_price_dict['close']))
		p_change_msg = get_color("%.2f" % price_dict[code]['p_change'])+'\t'+\
			get_color("%.2f" % sh_price_dict['p_change'])

		dp_msg = '/'.join(str(i) for i in days_list_persent)+':\t'+'\t'.join([ get_color("%.2f" % data_list_dict[i]) for i in days_list_persent ])

		#up2down_msg = 'up/down:\t'+get_color("%.2f" % up2persent)+'\t'+ get_color("%.2f" % down2persent)
		#end_msg = persent_msg+'\t'+p_change_msg+'\t'+dp_msg+'\t'+up2down_msg+'\t'+share_msg
		end_msg = persent_msg+'\t'+p_change_msg+'\t'+dp_msg+'\t'+share_msg


		if data_list_dict[10] <= -10 and persent <= -80 and\
			(data_list_dict[10] > data_list_dict[5]):
			color('cyan',mid_msg,end_msg)
			act_buy_list.append(price_dict[code]['close'])
		elif data_list_dict[10] <= -6 and persent <= -50 and\
			(data_list_dict[10] > data_list_dict[5]):
			color('magenta',mid_msg,end_msg)
			act_buy_list.append(price_dict[code]['close'])
		elif ((persent >= 90 and sh_persent >= 90) or (persent >= 90 and\
			data_list_dict[10] >= 10)) and\
			(data_list_dict[10] < data_list_dict[5]):
			color('yellow',mid_msg,end_msg)
			act_sell_list.append(price_dict[code]['close'])
		elif price_dict[code]['p_change'] > 0:
			color('red',mid_msg,end_msg)
		elif price_dict[code]['p_change'] < 0:
			color('green',mid_msg,end_msg)

		price_list.append(price_dict[code]['close'])
		day_count +=1

	price_avg = sum(price_list)/len(price_list)
	price_min = min(price_list)
	price_max = max(price_list)

	act_max = (min(act_sell_list) + max(act_sell_list))/2
	act_min = (min(act_buy_list) + max(act_buy_list))/2
	price_income = int((act_max - act_min)/act_min * 100)

	price_msg = 'min/max/avg/now:\t'+("%.2f" % price_min)+'\t'+("%.2f" % price_max)+'\t'+("%.2f" % price_avg)+'\t'+("%.2f" % now_price)
	act_msg = 'buy/sell:\t'+("%.2f" % act_min)+'\t'+("%.2f" % act_max)
	income_msg = 'income:\t'+get_color(str(price_income))+' %'

	print(code+'\t'+price_msg+'\t'+act_msg+'\t'+income_msg)

if __name__ == "__main__":

	colorama.init()
	stock_code = sys.argv[1]
	num4days = 420

	day_list = [i for i in range(5,180,5)]
	#day_list.append(3)

	now = datetime.date.today()
	d = datetime.datetime.now()
	d = d.replace(hour = 15,minute = 00,second = 0)

	if datetime.datetime.now() > d:
		yestoday = now
	else:
		yestoday = now - datetime.timedelta(days=1)

	start_day = now - datetime.timedelta(days=num4days+max(day_list)*2)
	end_day = yestoday

	do_it(stock_code,start_day,end_day,sorted(day_list))
