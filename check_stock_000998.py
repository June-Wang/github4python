import sys
import tushare as ts
import datetime

my_day = sys.argv[1]
#today = datetime.date.today()
today = sys.argv[1]
date_to3week_ago = sys.argv[2]
date_to10days_ago = sys.argv[3]
yestday = sys.argv[4]

my_date = today

#my_stock = ts.get_realtime_quotes('000998')
#my_stock_price = float(my_stock.price[0])
#my_date = my_stock.date[0]

df = ts.get_tick_data('000998',date=today)
my_stock_price_avg = df.price.sum()/len(df.price)
my_stock_price_min = df.price.min()
my_stock_price_max = df.price.max()

#to3week_ago = today + datetime.timedelta(weeks=-3)
#date_to3week_ago = to3week_ago.strftime('%Y-%m-%d')

#to1month_ago = today + datetime.timedelta(weeks=-4)
#date_to1month_ago = to1month_ago.strftime('%Y-%m-%d')


#print(my_pre_3week_num)
#my_pre_1month = ts.get_hist_data('000998', ktype='D',start=str(date_to1month_ago),end=str(my_day))[['p_change']].sum()[0]

if my_stock_price_avg == my_stock_price_avg:
	my_pre_3week = ts.get_hist_data('000998', ktype='D',start=str(date_to3week_ago),end=str(my_day))[['p_change']].sum()
	my_pre_3week_num = my_pre_3week[0]
	df = ts.get_tick_data('000998',date=yestday)
	my_stock_price_avg_yestday = (df.price.min() + df.price.max())/2
#	my_pre_date_to10days = ts.get_hist_data('000998', ktype='D',start=str(date_to10days_ago),end=str(my_day))[['p_change']].sum()
#	my_pre_date_to10days_num = my_pre_date_to10days[0]
	#green
	if my_stock_price_avg_yestday > my_stock_price_avg:
		if my_pre_3week_num <= -25: 
			sell_price_20 = my_stock_price_avg*20/100 + my_stock_price_avg
			print(my_date+' p_change:\t'+("%.2f" % my_pre_3week_num)+'\tprice_avg: '+("%.2f" % my_stock_price_avg)+'\tprice_min: '+("%.2f" % my_stock_price_min)+'\tprice_max: '+("%.2f" % my_stock_price_max)+'\tsell20: '+("%.2f" % sell_price_20))
		elif my_pre_3week_num <= -20:
			sell_price_15 = my_stock_price_avg*15/100 + my_stock_price_avg
			print(my_date+' p_change:\t'+("%.2f" % my_pre_3week_num)+'\tprice_avg: '+("%.2f" % my_stock_price_avg)+'\tprice_min: '+("%.2f" % my_stock_price_min)+'\tprice_max: '+("%.2f" % my_stock_price_max)+'\tsell15: '+("%.2f" % sell_price_15))
		elif my_pre_3week_num <= -15:
			sell_price_10 = my_stock_price_avg*10/100 + my_stock_price_avg
			print(my_date+' p_change:\t'+("%.2f" % my_pre_3week_num)+'\tprice_avg: '+("%.2f" % my_stock_price_avg)+'\tprice_min: '+("%.2f" % my_stock_price_min)+'\tprice_max: '+("%.2f" % my_stock_price_max)+'\tsell10: '+("%.2f" % sell_price_10))
		else:	
			print(my_date+' p_change:\t'+("%.2f" % my_pre_3week_num)+'\tprice_avg: '+("%.2f" % my_stock_price_avg)+'\tprice_min: '+("%.2f" % my_stock_price_min)+'\tprice_max: '+("%.2f" % my_stock_price_max))
