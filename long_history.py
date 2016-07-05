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

#def get_basics_info(code,basics):
#	stock_basics = {}
#	name = basics[basics.index == code][['name']].values[0]
#	industry = str(basics[basics.index == code][['industry']].values[0][0]) #行业
#	area = str(basics[basics.index == code][['area']].values[0][0]) #区域
#	pe = str(basics[basics.index == code][['pe']].values[0][0]) #市盈率
#	try:
#		pb = str(basics[basics.index == code][['pb']].values[0][0]) #市净率
#	except:
#		pb = 0.0
#	stock_basics[code] = {'name':name,'industry':industry,'area':area,'pe':pe,'pb':pb}
#	return(stock_basics[code])

def get_price_info(code,df,day_count):
	date = df.index.values[day_count]
	price = {}
	price_open = df[df.index == date].open[0] #开盘价格
	price_close = df[df.index == date].close[0] #开盘价格
	price_min = df[df.index == date].low[0] #当日最低
	price_max = df[df.index == date].high[0] #当日最高
	p_change = df[df.index == date].p_change[0] #当日股票涨幅
	price[code] = {'open':price_open,'close':price_close,'min':price_min,'max':price_max,'p_change':p_change}
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
			if count in day_list:
				data_list[count] = change_sum
		else:
			break
	#print(len(data_list))
	return(data_list,len(data_list))

#def p_change_persent(df):
#	count = 0
#	num4up = 0
#	for date_today in df.index.values:
#		date_yestoday=str(datetime.datetime.strptime(date_today, '%Y-%m-%d') + datetime.timedelta(days = -1))[:10]
#		#print(date_today,date_yestoday)
#		try:
#			p_change = df[df.index == date_today].p_change[0]
#		except:
#			continue
#
#		if p_change != p_change:
#			continue
#		
#		count +=1
#		if p_change >0:
#			num4up +=1
#	up_persent = num4up/count*100
#	return(up_persent)

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

#def color4msg(df,code,day_count,stock_basics_dict,price_dict,sh_price_dict,persent,sh_persent):
def color4msg(df,code,day_count,price_dict,sh_price_dict,persent,sh_persent):
	#date = str(yestoday)[:10]
	
	date = df.index.values[day_count]
	head_msg = date + '\t'+'P(min/max/close):'
	mid_msg = head_msg+'\t'+("%.2f" % price_dict[code]['min'])+'\t'+("%.2f" % price_dict[code]['max'])+'\t'+("%.2f" % price_dict[code]['close'])
	persent_msg = get_color(("%.2f" % persent))+'\t'+get_color(("%.2f" % sh_persent))+'\t'+str(int(sh_price_dict['close']))
	p_change_msg = get_color("%.2f" % price_dict[code]['p_change'])+'\t'+get_color("%.2f" % sh_price_dict['p_change'])
	end_msg = persent_msg+'\t'+p_change_msg

	if persent <=-85 or (sh_persent <= -90 and persent <= 0):
		color('cyan',mid_msg,end_msg)
	elif (persent > -85 and persent <= -70) or ((sh_persent > -90 and sh_persent <=-80) and persent < -60):
		color('magenta',mid_msg,end_msg)
	elif persent >= 90 and sh_persent >= 80:
		color('yellow',mid_msg,end_msg)
	elif price_dict[code]['p_change'] > 0:
		color('red',mid_msg,end_msg)
	elif price_dict[code]['p_change'] < 0:
		color('green',mid_msg,end_msg)

def do_it(code,basics,yestoday,end_day,day_list):

	#stock_basics_dict = {}
	#stock_basics_dict[code] = get_basics_info(code,basics)

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
	for day in df.index.values:
		try:
			price_dict[code] = get_price_info(code,df,day_count)
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
		#color4msg(df,code,day_count,stock_basics_dict,price_dict,persent,sh_persent)
		#color4msg(df,code,day_count,stock_basics_dict,price_dict,sh_price_dict,persent,sh_persent)
		color4msg(df,code,day_count,price_dict,sh_price_dict,persent,sh_persent)
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
