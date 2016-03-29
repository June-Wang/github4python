#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import pandas as pd
import sqlalchemy as sa
import mysql.connector
import colorama
from colorama import Fore, Back, Style
from termcolor import colored, cprint

colorama.init()

stock_table = 'tbl_p_change'
stock_code = sys.argv[1]

def get_color(text):
    my_number = float(text)
    if my_number > 0:
        my_text = colored(text, 'red')
    elif my_number < 0:
        text = str(abs(my_number))
        my_text = colored(text, 'green')
    else:
        my_text = text
    return(my_text)

#cursor = conn.cursor()
conn = sa.create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock')
sql = '''SELECT * FROM tbl_stock_change where stock_id = %s order by date DESC limit 100;'''
#rows = conn.execute(sql,stock_table,stock_code)
rows = conn.execute(sql,stock_code)

for row in rows:
    date_now = str(row[1])
    stock_id = row[2]
    open = row[3]
    close = row[4]
    price_min = row[5]
    price_max = row[6]
    p_change = row[7]
    p_change_3 = row[8]
    p_change_5 = row[9]
    p_change_10 = row[10]
    p_change_15 = row[11]
    p_change_20 = row[12]
    p_change_30 = row[13]
    p_change_60 = row[14]
    p_change_90 = row[15]
    p_change_120 = row[16]
    p_change_160 = row[17]
    p_change_avg5 = row[18]
    p_change_avg10 = row[19]
    p_change_avg20 = row[20]

    price_msg = 'price(min/max): '+("%.2f" % price_min)+' '+("%.2f" % price_max)
    p_change_title = 'change(1/3/5/10/15/20/30/60/90):\t'
    change_list = (p_change,p_change_3,p_change_5,p_change_10,
    p_change_15,p_change_20,p_change_30,p_change_60,p_change_90)
    p_change_msg = ''
    for change_f in change_list:
        p_change_msg = p_change_msg + get_color(str(change_f))+'\t'
    if p_change <0 and p_change_3 < 0 and p_change_5 < 0 and p_change_15 <0 and p_change_20 <0 \
    and p_change_30 <0 and p_change_60 > -20 and p_change_60 < 0:
        print(Fore.CYAN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
    elif (p_change < 0 and p_change_3 > 0 and p_change_5 > 9 and p_change_10 > 0 and p_change_15 >0 \
    and p_change_20 >0 and p_change_30 >0 and p_change_60 >0) or \
    (p_change < 0 and p_change_3 > 0 and p_change_5 > 0 and p_change_10 > 0 and p_change_15 >0 and \
    p_change_20 >0 and p_change_30 >0 and p_change_60 >0 and p_change_90<15 and p_change_90 >10):
        print(Fore.YELLOW+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
    elif p_change > 0:
        print(Fore.RED+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
    elif p_change < 0:
        print(Fore.GREEN+date_now+' '+price_msg+' '+p_change_title+Style.RESET_ALL+p_change_msg)
    else:
        print(date_now+' '+price_msg+' '+p_change_title+p_change_msg)
    #print(date,low,high,p_change)
