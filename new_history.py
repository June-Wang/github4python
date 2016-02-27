#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime

stock_code = sys.argv[1]
stock_code_p_change = float(sys.argv[2])

now = datetime.date.today()

for num in range(150):
	my_date = now - datetime.timedelta(days=num)
	B1_days = num+1
	B20_days = num+21
	yestoday = now - datetime.timedelta(days=B1_days)
	date_20days_ago = now - datetime.timedelta(days=B20_days)
	trans_msg = ''
	
	df = ts.get_tick_data(stock_code,date=my_date)
	price = df.price[0]
	if price != price:
		continue
	df = ts.get_hist_data(stock_code,start=str(date_20days_ago),end=str(my_date))
	price = df.close[0]
	yestoday_price = df.close[1]
	volume = df.volume[0]
	volume_avg20 = df.volume.sum()/len(df.volume)
	volume_avg20_change = (volume - volume_avg20)/volume_avg20 * 100
	price_min = df.low[0]
	price_max = df.high[0]
	price_avg_5 = df.ma5[0]
	price_avg_10 = df.ma10[0]
	price_avg_20 = df.ma20[0]
	p_change = df.p_change[0]
	p_change_5_avg = (price - price_avg_5)/price_avg_5 * 100
	p_change_10_avg = (price - price_avg_10)/price_avg_10 * 100
	p_change_20_avg = (price - price_avg_20)/price_avg_20 * 100

	date_now = str(my_date)
	price_msg = 'price(now/5/10/20/): '+("%.2f" % price)+' '+("%.2f" % price_avg_20)#+' '+("%.2f" % price_min)+' '+("%.2f" % price_max)
	p_change_msg = 'change(now/5/10/20):\t'+("%.2f" % p_change)+'\t'+("%.2f" % p_change_5_avg)+'\t'+("%.2f" % p_change_10_avg)+'\t'+("%.2f" % p_change_20_avg)
	volume_msg = 'volume(now/20): '+ str(volume)+'\t'+("%.2f" % volume_avg20_change)
	print(date_now+' '+price_msg+' '+p_change_msg+'\t'+volume_msg)
