import sys
import tushare as ts
import datetime

stock_code = '000998'
now = datetime.date.today()
#yestoday = now - datetime.timedelta(days=1)
#to3week_ago = today + datetime.timedelta(weeks=-3)

for num in range(60):
	my_date = now - datetime.timedelta(days=num)
	B1_days = num+1 
	B20_days = num+20
	yestoday = now - datetime.timedelta(days=B1_days)
	date_20days = now - datetime.timedelta(days=B20_days)
	msg = ''

	df = ts.get_tick_data(stock_code,date=my_date)
	stock_price_avg = df.price.sum()/len(df.price)
	if stock_price_avg != stock_price_avg:
		continue
	df = ts.get_hist_data(stock_code, ktype='D',start=str(date_20days),end=str(my_date))
	p_change_20days = df.p_change.sum()

	#df = ts.get_tick_data(stock_code,date=str(yestoday))
	#yestday_price_avg = df.price.sum()/len(df.price)
	
	df = ts.get_hist_data(stock_code,start=str(date_20days),end=str(my_date))
	price_avg_20days = df.close.sum()/len(df.close)

	if p_change_20days <= -20 and price_avg_20days > stock_price_avg:
		stock_price_sell = 0.15*stock_price_avg+stock_price_avg
		msg = 'buy: '+("%.2f" % stock_price_avg)+' sell: '+("%.2f" % stock_price_sell)
	print(str(my_date)+' price_avg: '+("%.2f" % stock_price_avg)+' p_change(20):\t'+("%.2f" % p_change_20days)+' '+msg)
