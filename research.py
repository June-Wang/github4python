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

def job4persent(stock_code,stock_basics,start_day,end_day,day_list,cycle_time):
    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
    persent_dict = get_persent_dict(df_hist_data,day_list,cycle_time)
    #print(persent_dict[0])
    get_stock_info(stock_code,stock_basics,df_hist_data,end_day)
    stock_info = get_stock_info(stock_code,stock_basics,df_hist_data,end_day)
    #print(persent_dict[0])
    stock_info.append(int(float(persent_dict[0])))
    return(stock_info)

def get_stock_basics():
    """
    获取所有股票的基本信息
    """
    try:
        stock_basics = ts.get_stock_basics()
    except:
        print('get_stock_basics timeout!')
        sys.exit(1)
    return(stock_basics)

def get_stock_info(stock_code,stock_basics,df_hist_data,end_day):
    """
    获取最后一天的股票信息
    """
    date = str(end_day)[:10]
    name = stock_basics[stock_basics.index == stock_code][['name']].values[0][0]
    industry = stock_basics[stock_basics.index == stock_code][['industry']].values[0][0]
    lastday = df_hist_data.index.values[0]
    close = ("%.2f" % df_hist_data[df_hist_data.index == lastday].close[0])
    output_args = [date,stock_code,name,close,industry]
    #print(msg)
    return(output_args)

def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    val = int(val)
    if val > 0:
        color = 'red'
    elif val < 0:
        color = 'green'
    else:
        color = 'black'
    #color = 'red' if val > 0 elif < 0 'green' else 'black'
    return 'color: %s' % color

if __name__ == "__main__":

    file = sys.argv[1]
    stock_list = get_stock_list(file)
    stock_basics=get_stock_basics()

    num4days = 90
    cycle_time = 30
    day_list = [i for i in range(cycle_time)]
    #stock_code = sys.argv[1]

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)

    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpus)

    results = []
    for stock_code in sorted(stock_list):
        persent = pool.apply_async(job4persent,(stock_code,stock_basics,start_day,end_day,day_list,cycle_time))
        #results.append(result.get())
        #print(stock_code,result.get())
        results.append(persent.get())
    pool.close()
    pool.join()

    #print(results)
    df = pd.DataFrame(results,columns=['日期','代码','名称','价格','行业','权重'])
    s = df.style.applymap(color_negative_red,subset=pd.IndexSlice[:, ['权重']]).render()
    print(s)
