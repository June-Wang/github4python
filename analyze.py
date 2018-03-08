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

def get_start_day(now,num4days,day_list):
    """
    获取时间周期的开始时间
    """
    start_day = now - datetime.timedelta(days=num4days+max(day_list))
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

def get_cycle_p_change_list(df_hist_data,day_list):
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

def get_cycle_date_list(df_hist_data,day_list):
    """
    生成周期内交易日期[返回列表]
    """
    cycle_date_list = list()
    for day in day_list:
        day_time = df_hist_data.index.values[day]
        cycle_date_list.append(day_time)
    return(cycle_date_list)

if __name__ == "__main__":

    #file = sys.argv[1]
    #stock_list = get_stock_list(file)
    stock_list = ['000998']
    #print(stock_list)
    #sys.exit(1)

    num4days = 160
    cycle_time = 30
    day_list = [i for i in range(0,cycle_time+1)]
    #day_list = [i for i in range(5,30)]
    #print(day_list)

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days,day_list)

    stock_code = '000998'
    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
    #print(start_day,end_day)
    #print(df_hist_data)
    cycle_p_change_list = get_cycle_p_change_list(df_hist_data,day_list)
    print(cycle_p_change_list)

    cycle_date_list = get_cycle_date_list(df_hist_data,day_list)
    print(cycle_date_list)

    #info_list = np.vstack(cycle_date_list) + np.vstack(cycle_p_change_list)
    info = pd.Series((cycle_p_change_list),index = cycle_date_list)
    print(info)
