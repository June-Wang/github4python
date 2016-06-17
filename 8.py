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

def p_change_persent(df):
	count = 0
	num4up = 0
	for date_today in df.index.values:
		date_yestoday=str(datetime.datetime.strptime(date_today, '%Y-%m-%d') + datetime.timedelta(days = -1))[:10]
		#print(date_today,date_yestoday)
		try:
			p_change = df[df.index == date_today].p_change[0]
		except:
			continue

		if p_change != p_change:
			continue
		
		count +=1
		if p_change >4:
			num4up +=1
	up_persent = num4up/count*100
	return(up_persent)

def do_it(code,basics):

	num4days = 15
	now = datetime.date.today()
	yestoday = now - datetime.timedelta(days=1)
	end_day = now - datetime.timedelta(days=num4days)

	stock_basics_dict = {}
	stock_basics_dict[code] = get_basics_info(code,basics)

	try:
		df = ts.get_hist_data(code,start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)

	up_persent = p_change_persent(df)
	down_persent = -100.00+up_persent

	if up_persent >= 40:
		msg_head = get_color(("%.2f" % up_persent))
		msg_mid = code+'\t'+stock_basics_dict[code]['name']
		msg_end = '行业\t'+stock_basics_dict[code]['industry']+'\t'+'市盈率\t'+stock_basics_dict[code]['pe']
		print(msg_head+'\t'+msg_mid+'\t'+msg_end)
	elif down_persent <= -80:
		msg_head = get_color(("%.2f" % down_persent))

	#	msg_head = '[up/down]\t'+get_color(("%.2f" % up_persent))+'\t'+get_color(("%.2f" % down_persent))

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
