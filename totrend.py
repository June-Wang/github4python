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
	stock = {}
	info_list = ['name','industry','pe']
	for key in info_list:
		stock[key] = str(basics[basics.index == code][[key]].values[0][0])
	return(stock)	

def get_days(num4days):
	now = datetime.date.today()
	yestoday = now - datetime.timedelta(days=1)
	end_day = now - datetime.timedelta(days=num4days)
	workday = pd.bdate_range(start=str(end_day),end=str(yestoday))
	days_list = [now,yestoday,end_day,workday]
	return(days_list)

def get_p_trend(df,df_sh):
	p = 0
	p_up = 0
	p_down = 0
	p_sh = 0
	p_sh_up = 0
	p_sh_down = 0
	count = 0
	for today in df.index.values:
		count +=1
		p_change = df[df.index == today].p_change[0]
		p_change_sh = df_sh[df_sh.index == today].p_change[0]
		if p_change >=0:
			p +=1
			p_up +=1
		else:
			p -=1
			p_down -=1

		if p_change_sh >=0:
			p_sh +=1
			p_sh_up +=1
		else:
			p_sh -=1
			p_sh_down -=1

	p_up_p = p_up/count *100
	p_down_p = p_down/count*100
	p_sh_up_p = p_sh_up/count*100
	p_sh_down_p = p_sh_down/count*100
	return(p,p_up_p,p_down_p,p_sh,p_sh_up_p,p_sh_down_p)

def do_it(code,basics):
	stock_code = code
	num4days = 60
	now,yestoday,end_day,workday = get_days(num4days)
	stock = get_basics_info(code,basics)

	try:
		df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
		df_sh = ts.get_hist_data('sh',start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)

	#p_trend,p_sh_trend = get_p_trend(df,df_sh)
	p,p_up_p,p_down_p,p_sh,p_sh_up_p,p_sh_down_p = get_p_trend(df,df_sh)
	count = p - p_sh
	persent = p/count *100
	if p_sh < p and count >=15:
		msg_list = list()
		for key in ['name','industry','pe']:
			msg_list.append(str(stock[key]))
		#name  = stock['name']
		#industry = stock['industry']
		#pe = stock['pe']
		msg = '\t'.join(msg_list)
		persent_msg = get_color(str(p))+'\t'+get_color(str((p_sh)))+'\t'+ get_color(("%.2f" % persent))
		print(persent_msg+'\t'+stock_code+'\t'+msg)
		
if __name__ == "__main__":
	colorama.init()

	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('timeout!')
		sys.exit(1)

	#stock_list = stock_basics[stock_basics.pe >= 80].index.values
	stock_list = stock_basics.index.values
	pool = multiprocessing.Pool(processes=4)
	
	for stock_code in sorted(stock_list):
		pool.apply_async(do_it, (stock_code,stock_basics))
	pool.close()
	pool.join()
