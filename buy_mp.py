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

def color4rules(day_data,p_change_list,price_open,p_change):
	if day_data[5] == day_data[10] or day_data[3] == day_data[5] or day_data[10] == day_data[15] or day_data[15] == day_data[20]:
		output_color = 'no'
	elif day_data[3] > 20:
		output_color = 'yellow'
	elif day_data[5] > -15 or price_open >= 15 or day_data[3] > 0 or day_data[5] > 0:
		output_color = 'no'
	elif day_data[3] <= -20 and p_change < 9:
		output_color = 'cyan'
	elif day_data[10] < 0 and day_data[15] < 0  and day_data[20] < 0 and day_data[30] < 0 and day_data[60] < 0 and day_data[90] < 0 and day_data[120] < 0:
		output_color = 'cyan'
#	elif p_change < 0 and day_data[3] > 0 and day_data[5] >0 and day_data[10] >0 and day_data[20] >0 and day_data[30] >0 and day_data[60] >0:
#		print(Fore.YELLOW+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
#	elif p_change > 0:
#		print(Fore.RED+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
#	elif p_change < 0:
#		print(Fore.GREEN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	else:
		output_color = 'no'
	return(output_color)

def color4output(date_now,color,day_list,p_change_list,stock_code,stock_name,price_open,p_change,price_min,price_max):
	day_msg = '1/'+'/'.join(str(day) for day in day_list)
	price_msg = 'P(min/max):\t'+("%.2f" % price_min)+' '+("%.2f" % price_max)
	p_change_title = 'C('+day_msg+'):\t'
	p_change_msg = get_color(("%.2f" % p_change))
	for p_change_value in p_change_list:
		p_change_msg += '\t'+ get_color(("%.2f" % p_change_value))
	if color == 'yellow':
		print(stock_code +" "+stock_name+"\t"+Fore.YELLOW+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	elif color == 'cyan':
		print(stock_code +" "+stock_name+"\t"+Fore.CYAN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	elif color == 'red':
		print(stock_code +" "+stock_name+"\t"+Fore.RED+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	elif color == 'green':
		print(stock_code +" "+stock_name+"\t"+Fore.GREEN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
	else:
		print(stock_code +" "+stock_name+"\t"+date_now+' '+price_msg+' '+p_change_title+p_change_msg)

def do_it(code,basics):
	stock_name = str(basics[basics.index == code][['name']].values[0][0])
	stock_code = code
	num4days = 1
	now = datetime.date.today()
	yestoday = now - datetime.timedelta(days=1)
	end_day = now - datetime.timedelta(days=num4days+121)
	workday = pd.bdate_range(start=str(end_day),end=str(yestoday))
	
	try:
		df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
	except:
		print('timeout!')
		sys.exit(1)	
	
	days = len(workday.date)
	
	for i in range(days-1,days-2,-1):
		my_str = ''
		date_today = str(workday.date[i])
		date_yestoday = str(workday.date[i-1])
		date_now = date_today
	
		try:
			price_open = df[df.index == date_today].open[0]
			yestoday_price_open = df[df.index == date_yestoday].open[0]
		except:
			#print(date_now,'no data!')	
			continue
	
		if price_open != price_open:
			continue
	
		price_open = df[df.index == date_today].open[0]
		price_min = df[df.index == date_today].low[0]
		price_max = df[df.index == date_today].high[0]
		p_change = df[df.index == date_today].p_change[0]
	
		p_change_list = get_p_change_for_days(get_day(121,i,workday),df,day_list)
		day_data = get_day_data(p_change_list,day_list)
		#print(stock_code,day_data[5],day_data[10])

		color = color4rules(day_data,p_change_list,price_open,p_change)	
		if color != 'no':
			color4output(date_now,color,day_list,p_change_list,stock_code,stock_name,price_open,p_change,price_min,price_max)

if __name__ == "__main__":

	colorama.init()
	day_list = [3,5,10,15,20,30,60,90,120]
	
	try:
		stock_basics = ts.get_stock_basics()
	except:
		print('timeout!')
		sys.exit(1)
	
	stock_list = stock_basics.index.values
	
	pool = multiprocessing.Pool(processes=8)
	for stock_code in stock_list:
			#p = multiprocessing.Process(target=do_it,args=(stock_code,stock_basics))
			#p.start()
		pool.apply_async(do_it, (stock_code,stock_basics))
	pool.close()
	pool.join()