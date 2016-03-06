#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime

stock_code = sys.argv[1]
stock_code_p_change = float(sys.argv[2])

now = datetime.date.today()

for num in range(200):
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
	volume = df.volume[0]
	#volume_avg20 = df.volume.sum()/len(df.volume)
	#volume_avg20_change = (volume - volume_avg20)/volume_avg20 * 100
	price_min = df.low[0]
	price_max = df.high[0]
	price_avg_5 = df.ma5[0]
	price_avg_10 = df.ma10[0]
	price_avg_20 = df.ma20[0]
	p_change = df.p_change[0]
	p_change_5_avg = (price - price_avg_5)/price_avg_5 * 100
	p_change_10_avg = (price - price_avg_10)/price_avg_10 * 100
	p_change_20_avg = (price - price_avg_20)/price_avg_20 * 100

	yestoday_price = df.close[1]
	yestoday_price_avg_10 = df.ma10[1]
	yestoday_p_change_10_avg = (yestoday_price - yestoday_price_avg_10)/yestoday_price_avg_10 * 100

	df = ts.get_sina_dd(stock_code, date=str(my_date))
	
	try: 
		#len(df.type)
		types = sorted(set(df.type))
		type_sum = df['volume'].sum()
		type_sum_count = len(df)
		#s_out = ''
		stock_type_count = dict()
		stock_type_change = dict()
		stock_type_volume = dict()
		for s_type in types:
			stock_type_count[s_type] = df['type'][df.type == s_type].count()
			stock_type_volume[s_type] = df['volume'][df.type == s_type].sum()
			stock_type_change[s_type] = stock_type_volume[s_type]/type_sum*100
	
		stock_type_count_msg = ''
		stock_type_change_msg = ''
		for s_type in types:
			#stock_type_count_msg = stock_type_count_msg+'\t'+str(s_type)+'\t'+str(stock_type_count[s_type])+'\t'
			stock_type_change_msg = stock_type_change_msg+'\t'+str(s_type)+'\t'+("%.2f" % stock_type_change[s_type])+'%'
			
		stock_type_change_msg = stock_type_change_msg + ' 总数: '+ str(type_sum_count)
	except:
		#continue
		stock_type_change_msg = ''
	#print(stock_type_change_msg)

	act_msg = ''
	#if p_change_5_avg < 0 and p_change_5_avg > p_change_10_avg and p_change_10_avg > p_change_20_avg and p_change_10_avg <= (stock_code_p_change*-100):
	if p_change > p_change_5_avg and p_change_5_avg > p_change_10_avg and p_change_10_avg <= (stock_code_p_change*-1) and p_change_10_avg < yestoday_p_change_10_avg:
		act_msg = 'buy'

	date_now = str(my_date)
	price_msg = 'price(1/5/10): '+("%.2f" % price)+' '+("%.2f" % price_avg_5)+' '+("%.2f" % price_avg_10)
	#+' '+("%.2f" % price_min)+' '+("%.2f" % price_max)
	p_change_msg = 'change(1/5/10):\t'+("%.2f" % p_change)+'\t'+("%.2f" % p_change_5_avg)+'\t'+("%.2f" % p_change_10_avg)#+'\t'+("%.2f" % p_change_20_avg)
	print(date_now+' '+price_msg+' '+p_change_msg+'\t'+stock_type_change_msg+' '+act_msg)
