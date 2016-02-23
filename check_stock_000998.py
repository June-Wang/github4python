import sys
import tushare as ts
import datetime

my_day = sys.argv[1]
#today = datetime.date.today()
today = sys.argv[1]

#my_stock = ts.get_realtime_quotes('000998')
#my_stock_price = float(my_stock.price[0])
#my_date = my_stock.date[0]

df = ts.get_tick_data('000998',date=today)
my_stock_price = df.price.min()
my_date = today

sell_price = my_stock_price*20/100 + my_stock_price

#to3week_ago = today + datetime.timedelta(weeks=-3)
#date_to3week_ago = to3week_ago.strftime('%Y-%m-%d')

#to1month_ago = today + datetime.timedelta(weeks=-4)
#date_to1month_ago = to1month_ago.strftime('%Y-%m-%d')

date_to3week_ago = sys.argv[2]

my_pre_3week = ts.get_hist_data('000998', ktype='D',start=str(date_to3week_ago),end=str(my_day))[['p_change']].sum()
my_pre_3week_num = my_pre_3week[0]
print(my_pre_3week_num)
#my_pre_1month = ts.get_hist_data('000998', ktype='D',start=str(date_to1month_ago),end=str(my_day))[['p_change']].sum()[0]

if my_pre_3week_num <= -25:
	if my_stock_price:
		print(my_date+' price:'+("%.2f" % my_stock_price)+' sell:'+("%.2f" % sell_price))
#and my_pre_1month <= -20:
