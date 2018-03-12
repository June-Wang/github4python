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

def get_stock_list(file):
    """
    从文件获取股票列表
    """
    if not os.path.isfile(file):
        print(file,'not found!')
        sys.exit(1)

    with open(file,"r") as fh:
        rows = fh.readlines()
    #print(rows)

    stock_list = list()
    for code in rows:
        m = re.match("^\d{6}$",code)
        if not m:
            continue
        stock_code = code.replace("\n", "")
        stock_list.append(stock_code)
    #print(stock_list)
    return(stock_list)

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

def get_persent_dict(df_hist_data,day_list,cycle):
    date_list = [i for i in range(1,cycle)]
    #print(len(date_list))
    day_persent = dict()
    days_persent_list = list()
    for date in date_list:
        day_persent[date] = get_cycle_p_change_list(df_hist_data,day_list,date)

    persent_dict = dict()
    for day in day_list:
        count = 0
        for date in date_list:
            if float(day_persent[date][day]) > 0:
                count = count +1
            else:
                count = count -1
        result = count / len(date_list) * 100
        persent_dict[day] = ("%.2f" % result)
    return(persent_dict)

if __name__ == "__main__":

    num4days = 90

    stock_code = sys.argv[1]

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)
    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
    
    day_list = [i for i in range(30)]
    #cycle_p_change_list = get_cycle_p_change_list(df_hist_data,day_list,30)
    persent_dict = get_persent_dict(df_hist_data,day_list,30)
    print(persent_dict[0])
