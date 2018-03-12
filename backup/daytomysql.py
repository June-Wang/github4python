#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd
import sqlalchemy as sa
import mysql.connector

stock_code = sys.argv[1]
#stock_code = '600519'
#stock_code_p_change = float(sys.argv[2])

class NumpyMySQLConverter(mysql.connector.conversion.MySQLConverter):
    """ A mysql.connector Converter that handles Numpy types """

    def _float32_to_mysql(self, value):
        return float(value)

    def _float64_to_mysql(self, value):
        return float(value)

    def _int32_to_mysql(self, value):
        return int(value)

    def _int64_to_mysql(self, value):
        return int(value)

#conn = sa.create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock')
config = {
    'user'    : 'stockadmin',
    'host'    : 'localhost',
    'password': 'stock2016',
    'database': 'stock'
}

conn = mysql.connector.connect(**config)
conn.set_converter_class(NumpyMySQLConverter)
cursor = conn.cursor()

now = datetime.date.today()
yestoday = now - datetime.timedelta(days=1)
end_day = now - datetime.timedelta(days=165)
workday = pd.bdate_range(start=str(end_day),end=str(yestoday))

try:
    df = ts.get_hist_data(stock_code,start=str(end_day),end=str(yestoday))
except:
    print('timeout!')
    sys.exit(1)    

days = len(workday.date)

def get_day(day,loop_i):
    global workday
    num = day+2
    my_date_tmp = list()
    for my_day in range(loop_i-2,loop_i-num,-1):
        #print(my_day,str(workday.date[my_day]))
        my_date_tmp.append(str(workday.date[my_day]))
    return(my_date_tmp)

def get_p_change_for_days(date_list):
    global df
    my_change_sum = 0.0
    for my_date in date_list:
        try:
            my_change_tmp = float(df[df.index == my_date].p_change[0])
        except:
            my_change_tmp = 0.0
        my_change_sum += my_change_tmp
    return(my_change_sum)

date_today = str(workday.date[-1])
date_yestoday = str(workday.date[-2])
date_now = date_today

try:
    price_open = df[df.index == date_today].open[0]
    yestoday_price_open = df[df.index == date_yestoday].open[0]
except:
    print(date_now,'no data!')    
    sys.exit(1)

if price_open != price_open:
    print(date_now,'no data!')
    sys.exit(1)

volume = df[df.index == date_today].volume[0]
price_open = df[df.index == date_today].open[0]
price_close = df[df.index == date_today].close[0]
price_min = df[df.index == date_today].low[0]
price_max = df[df.index == date_today].high[0]
price_avg_5 = df[df.index == date_today].ma5[0]
price_avg_10 = df[df.index == date_today].ma10[0]
price_avg_20 = df[df.index == date_today].ma20[0]

i = days
p_change_3 = get_p_change_for_days(get_day(3,i))
p_change_5 = get_p_change_for_days(get_day(5,i))
p_change_10 = get_p_change_for_days(get_day(10,i))
p_change_15 = get_p_change_for_days(get_day(15,i))
p_change_20 = get_p_change_for_days(get_day(20,i))
p_change_30 = get_p_change_for_days(get_day(30,i))
p_change_60 = get_p_change_for_days(get_day(60,i))
p_change_90 = get_p_change_for_days(get_day(90,i))
p_change_120 = get_p_change_for_days(get_day(120,i))
p_change_160 = get_p_change_for_days(get_day(160,i))

p_change = df[df.index == date_today].p_change[0]
p_change_min = (price_min - price_open)/price_open * 100
p_change_max = (price_max - price_open)/price_open * 100
p_change_open = p_change_max + p_change_min
p_change_close = (price_min - price_close)/price_close * 100 + (price_max - price_close)/price_close * 100
p_change_avg_5 = (price_close - price_avg_5)/price_avg_5 * 100
p_change_avg_10 = (price_close - price_avg_10)/price_avg_10 * 100
p_change_avg_20 = (price_close - price_avg_20)/price_avg_20 * 100

yestoday_price_open = df[df.index == date_yestoday].open[0]
yestoday_price_close = df[df.index == date_yestoday].close[0]
yestoday_price_avg_5 = df[df.index == date_yestoday].ma5[0]
yestoday_price_avg_10 = df[df.index == date_yestoday].ma10[0]
yestoday_p_change_avg_5 = (yestoday_price_close - yestoday_price_avg_5)/yestoday_price_avg_5 * 100
yestoday_p_change_avg_10 = (yestoday_price_close - yestoday_price_avg_10)/yestoday_price_avg_10 * 100

ins = '''INSERT INTO tbl_stock_change 
    (date,stock_id,open,close,low,high,stock_change,stock_change3,stock_change5,stock_change10,stock_change15,stock_change20,stock_change30,stock_change60,stock_change90,stock_change120,stock_change160,stock_change_avg5,stock_change_avg10,stock_change_avg20) 
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

data_list = list()
my_str = ''

for my_str in (date_now,stock_code,price_open,price_close,price_min,price_max,p_change):
    data_list.append(my_str)
float_list= (p_change_3,p_change_5,p_change_10,p_change_15,p_change_20,p_change_30,p_change_60,p_change_90,p_change_120,p_change_160,p_change_avg_5,p_change_avg_10,p_change_avg_20)

for to2f in float_list:
    my_str = ("%.2f" % to2f)
    data_list.append(my_str)

try:
    #print(date_now,data_list)
    cursor.execute(ins,data_list)
except mysql.connector.errors.IntegrityError as msg:
    print(msg)
except mysql.connector.errors.ProgrammingError as msg:
    print(msg)
finally:
    cursor.close()
