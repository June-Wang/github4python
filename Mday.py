#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import colorama
from colorama import Fore, Back, Style

stock_code = sys.argv[1]
stock_code_p_change = float(sys.argv[2])

now = datetime.date.today()

yestoday = now - datetime.timedelta(days=1)
date_20days_ago = now - datetime.timedelta(days=20)
trans_msg = ''

df = ts.get_realtime_quotes(stock_code)
price = df.price[0]
if price != price:
	print('no data!')
	sys.exit(1)

stock_name = df.name[0]
stock_date = df.date[0] +' '+ df.time[0]
price_open = df.open[0]
price_min = df.low[0]
price_max = df.high[0]
p_change = (float(df.pre_close[0]) - float(price)) /float(df.pre_close[0])*-100

df = ts.get_hist_data(stock_code,start=str(date_20days_ago),end=str(yestoday))

yestoday_price = df.close[0]
yestoday_price_avg_5 = df.ma5[0]
yestoday_price_avg_10 = df.ma10[0]
yestoday_p_change_avg_5 = (yestoday_price - yestoday_price_avg_5)/yestoday_price_avg_5 * 100
yestoday_p_change_avg_10 = (yestoday_price - yestoday_price_avg_10)/yestoday_price_avg_10 * 100

#print(price,price_min,price_max,p_change,yestoday_price)
#sys.exit(1)

#if p_change_avg_5 < 0 and p_change_avg_5 > p_change_avg_10 and p_change_avg_10 > p_change_avg_20 and p_change_avg_10 <= (stock_code_p_change*-100):
#if p_change > p_change_avg_5 and p_change_avg_5 > p_change_avg_10 and p_change_avg_10 <= (stock_code_p_change*-1) and p_change_avg_10 < yestoday_p_change_avg_10:
#if p_change <= -4 and p_change_avg_10 <= -10:
#	act_msg = 'buy'
#if p_change > p_change_avg_5 and p_change_avg_5 > p_change_avg_10 and  yestoday_p_change_avg_10 <= (stock_code_p_change*-1) and p_change_avg_10 > yestoday_p_change_avg_10:
#	act_msg = 'buy'

price_msg = stock_date +' '+stock_name + ' open: '+("%.2f" % float(price_open)) + ' price: '+("%.2f" % float(price)) + ' p_change: '+("%.2f" % float(p_change))+'%'

if p_change > 0:
	print(Fore.RED+price_msg+Style.RESET_ALL)
elif p_change < 0:
	print(Fore.GREEN+price_msg+Style.RESET_ALL)
elif p_change < -6 and yestoday_p_change_avg_5 < -5 and yestoday_price_avg_10 > price_open:
	print(Fore.YELLOW+price_msg+Style.RESET_ALL)
else:
	print(price_msg)
