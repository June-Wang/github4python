#!/usr/local/bin/python3.4

import sys
import tushare as ts
import datetime

#stock_code = '000998'
stock_code = sys.argv[1]
stock_code_p_change = float(sys.argv[2])

now = datetime.date.today()
#yestoday = now - datetime.timedelta(days=1)
#to3week_ago = today + datetime.timedelta(weeks=-3)

for num in range(60):
	my_date = now - datetime.timedelta(days=num)
	B1_days = num+1 
	B20_days = num+30
	yestoday = now - datetime.timedelta(days=B1_days)
	date_20days_ago = now - datetime.timedelta(days=B20_days)
	trans_msg = ''

	df = ts.get_tick_data(stock_code,date=my_date)
	stock_price_avg = df.price.sum()/len(df.price)
	stock_price_min = df.price.min()
	stock_price_max = df.price.max()

	if stock_price_avg != stock_price_avg:
		continue
	df = ts.get_hist_data(stock_code, ktype='D',start=str(date_20days_ago),end=str(my_date))
	p_change_20days = df.p_change.sum()

	#df = ts.get_tick_data(stock_code,date=str(yestoday))
	#yestday_price_avg = df.price.sum()/len(df.price)
	
	df = ts.get_hist_data(stock_code,start=str(date_20days_ago),end=str(my_date))
	price_avg_20days = df.close.sum()/len(df.close)

	#if p_change_20days <= -20 and price_avg_20days > stock_price_avg:
	if price_avg_20days > stock_price_avg:
		stock_change_number = (price_avg_20days - stock_price_avg)/price_avg_20days
		if stock_change_number >= stock_code_p_change:
			stock_price_sell = stock_code_p_change*stock_price_avg+stock_price_avg
			trans_msg = ' buy: '+("%.2f" % stock_price_avg)+' sell: '+("%.2f" % stock_price_sell)

	date_now = str(my_date)
	p_change_str = ' p_change:\t'+("%.2f" % p_change_20days)
	stock_price_avg_str = ("%.2f" % stock_price_avg)	
	stock_price_avg_20days_str = ("%.2f" % price_avg_20days)	
	stock_price_min_str = ("%.2f" % stock_price_min)
	stock_price_max_str = ("%.2f" % stock_price_max)
	
	stock_price_msg = ' avg/avg_20d: '+stock_price_avg_str+'|'+stock_price_avg_20days_str+' min/max: '+stock_price_min_str+'|'+stock_price_max_str
	
	print(date_now+p_change_str+stock_price_msg+trans_msg)
