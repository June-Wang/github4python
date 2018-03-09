#!/usr/bin/env python3.4

import sys
import re
import os
import datetime
import time
import multiprocessing
import tushare as ts
import pandas as pd
import numpy as np
from colorama import Fore, Back, Style
from termcolor import colored, cprint

def get_end_day(now):
    """
    获取工作日的最后一天
    """
    d = datetime.datetime.now()
    d = d.replace(hour = 15,minute = 00,second = 0)

    if datetime.datetime.now() > d:
        end_day = now
    else:
        end_day = now - datetime.timedelta(days=1)
    return(end_day)

def get_start_day(now,num4days):
    """
    获取时间周期的开始时间
    """
    #start_day = now - datetime.timedelta(days=num4days+max(day_list))
    start_day = now - datetime.timedelta(days=num4days)
    return(start_day)

def get_df_hist_data(stock_code,start_day,end_day):
    """
    获取股票的历史数据，参数：股票代码(stock_code)、时间周期(num4days)
    开始时间(start_day)、结束时间(end_day)
    """
    try:
        df_hist_data = ts.get_hist_data(stock_code,start=str(start_day),end=str(end_day))
    except:
        print('get_hist_data timeout!')
        sys.exit(1)
    return(df_hist_data)

def get_cycle_p_change_list(df_hist_data,day_list,cycle_time):
    """
    生成周期内涨跌幅的值[返回列表]
    """
    cycle_p_change_list = list()
    for day in day_list:
        start_t = day
        end_t = day + cycle_time
        #print(start_t,end_t)
        cycle_p_change_sum = ("%.2f" % df_hist_data[['p_change']].values[start_t:end_t].sum())
        cycle_p_change_list.append(cycle_p_change_sum)
        #print(day_time,str(cycle_p_change_sum))
    return(cycle_p_change_list)

def get_p_change_grow_list(df_hist_data,day_list,cycle_time):
    """
    获取周期内涨跌幅的和
    """
    p_change_grow_list = list()
    for day in day_list:
        start_t = day
        end_t = day + cycle_time
        p_change_list = df_hist_data[['p_change']].values[start_t:end_t]
        count = 0
        for p_change in p_change_list:
            if p_change > 0:
                count = count + 1
            else:
                count = count - 1
        #print(count)
        result = count / len(p_change_list) * 100
        p_change_grow_list.append(int(result))
    return(p_change_grow_list)

def get_color(text):
    text_f = float(text)
    if text_f > 0:
        text_color = colored(text, 'red')
    elif text_f < 0:
        text_color = colored(text, 'green')
    else:
        text_color = text
    return(text_color)

def get_persent_sum_dict(df_hist_data,day_range):
    date_list = [i for i in range(5,day_range,5)]
    date_list.append(3)
    date_list = sorted(date_list)
    #print(len(date_list))
    day_persent = dict()
    days_persent_list = list()
    for date in date_list:
        day_persent[date] = get_cycle_p_change_list(df_hist_data,day_list,date)
        days_persent_list.append(np.dstack(day_persent[date]))
        #print(day_persent[date])

    #print(days_persent_list)
    persent_sum_dict = dict()
    for i in range(0,len(days_persent_list)):
        persent_sum_dict[i] = np.sum(days_persent_list[i][0].astype(np.float))/len(days_persent_list)
    print(persent_sum_dict)

    #return(days_persent_list)
    return(persent_sum_dict)

if __name__ == "__main__":

    #stock_list = ['000998']

    cycle_time = 30
    day_range = 90

    num4days = day_range + cycle_time + 60*2

    day_list = [i for i in range(0,day_range+1)]

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)

    stock_code = '000998'
    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
    #print(start_day,end_day)
    #print(df_hist_data)
    ###cycle_p_change_list = get_cycle_p_change_list(df_hist_data,day_list,cycle_time)
    #print(cycle_p_change_list)
    #print(len(cycle_p_change_list))

    #cycle_date_list = get_cycle_date_list(df_hist_data,day_list)
    #print(cycle_date_list)

    #info_list = np.vstack(cycle_date_list) + np.vstack(cycle_p_change_list)
    #info = pd.Series((cycle_p_change_list),index = cycle_date_list)
    #print(info)
    
    p_change_grow_list = get_p_change_grow_list(df_hist_data,day_list,cycle_time)
    #print(p_change_grow_list)
    #print(len(p_change_grow_list))

    #day_list_persent = [3,5,10,20,30,60]
    #cycle_p_change = dict()
    #for day in day_list_persent:
    #    cycle_p_change[day] = get_cycle_p_change_list(df_hist_data,day_list,day)
        #print(cycle_p_change_list[day])
    persent_sum_dict = get_persent_sum_dict(df_hist_data,day_range)
    #print(np.sum(list(days_persent_list[0][0])))
    sys.exit(0)

    for day in day_list:
        #persent = float(cycle_p_change_list[day])+float(p_change_grow_list[day])
        date = df_hist_data.index.values[day]
        price = df_hist_data[['close']].values[day][0]
        #front_msg = date +'\t'+ type(price)
        #print(type(price))

        ma_field = ['ma5','ma10','ma20']
        ma_list = [ df_hist_data[[field]].values[day][0] for field in ma_field ]
        ma_msg = '\t'.join([("%.2f" % field) for field in ma_list])
        #print(ma_msg)
        
        cycle_p_change_list = [ cycle_p_change[i][day] for i in day_list_persent ]
        #print(cycle_p_change_list)
        cycle_p_change_msg = '\t'.join([get_color(str(field)) for field in cycle_p_change_list])
        #print(cycle_p_change_msg)
        #color_field = [cycle_p_change_list[day],p_change_grow_list[day]]
        #print(color_field)
        
        #output_color = '\t'.join(get_color(str(field)) for field in color_field)
        print(date+"\t"+str(price)+"\t3/5/10/20/30/60\t"+cycle_p_change_msg+"\tMA\t"+ma_msg+"\t"+get_color(str(p_change_grow_list[day])))
