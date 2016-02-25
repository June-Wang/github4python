#!/usr/local/bin/python3.4

import sys
import tushare as ts
import datetime

stock_code = sys.argv[1]
#stock_code_p_change = float(sys.argv[2])

now = datetime.date.today()
yestoday = now - datetime.timedelta(days=1)
date_20days_ago = now - datetime.timedelta(days=30)

#df = ts.get_tick_data(stock_code,date=str(my_date))
df = ts.get_realtime_quotes(stock_code)
stock_price_now = float(df.price[0])
my_date = df.date[0]+' '+df.time[0]

df = ts.get_tick_data(stock_code,date=yestoday)
stock_price_now_yestoday = df.price.sum()/len(df.price)

if stock_price_now != stock_price_now:
	print('no data!')
	sys.exit(1)	

df = ts.get_hist_data(stock_code, ktype='D',start=str(date_20days_ago),end=str(yestoday))
#df = ts.get_hist_data(stock_code,start=str(date_20days_ago),end=str(yestoday))
p_change_20days = df.p_change.sum()
price_avg_20days = df.close.sum()/len(df.close)

stock_change_number_now = (price_avg_20days - stock_price_now)/price_avg_20days
stock_change_number_now_yestoday = (price_avg_20days - stock_price_now_yestoday)/price_avg_20days

date_now = str(my_date)
p_change_number = stock_change_number_now*100
p_change_number_str = ("%.2f" % p_change_number)
p_change_20days_str = ("%.2f" % p_change_20days)
stock_price_now_str = ("%.2f" % stock_price_now)	
stock_price_now_20days_str = ("%.2f" % price_avg_20days)	

stock_price_msg = ' change/change20d: '+p_change_number_str+'|'+p_change_20days_str+' now/avg20d: '+stock_price_now_str+'|'+stock_price_now_20days_str

print(date_now+stock_price_msg)
