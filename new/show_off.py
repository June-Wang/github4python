#!/usr/bin/env python3

import sys,re,os,datetime,time
import tushare as ts
import pandas as pd
import numpy as np
from colorama import Fore, Back, Style
from termcolor import colored, cprint
import urllib.request

def get_days(pro,start_day,end_day):
    """
    exchange	str	Y	交易所 SSE上交所 SZSE深交所
    cal_date	str	Y	日历日期
    is_open	str	Y	是否交易 0休市 1交易
    pretrade_date	str	N	上一个交易日
    """
    df_all_day = pro.query('trade_cal', start_date=start_day, end_date=end_day)
    all_day = df_all_day['cal_date']

    df_day_work = df_all_day[df_all_day['is_open']>0]
    day_work = df_day_work['cal_date']
    return(all_day,day_work,df_all_day,df_day_work)

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
    return(end_day.strftime("%Y%m%d"))

def get_start_day(now,num4days):
    """
    获取开始时间
    """
    start_day = now - datetime.timedelta(days=num4days)
    return(start_day.strftime("%Y%m%d"))

def get_df_hist_data(stock_code,start_day,end_day):
    """
    获取股票的历史数据，参数：股票代码(stock_code)、时间周期(num4days)
    开始时间(start_day)、结束时间(end_day)
    ts_code	str	股票代码
    trade_date	str	交易日期
    open	float	开盘价
    high	float	最高价
    low	float	最低价
    close	float	收盘价
    pre_close	float	昨收价
    change	float	涨跌额
    pct_chg	float	涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
    vol	float	成交量 （手）
    amount	float	成交额 （千元）
    """
    try:
        df_hist_data = df = pro.query('daily', ts_code=stock_code, start_date=start_day, end_date=end_day)
    except:
        print('get_hist_data timeout!')
        sys.exit(1)
    return(df_hist_data)

def get_change_list(df_hist_data,df_work_day,df_all_day,period,day_range):
    """
    生成周期内涨跌幅的值[返回列表]
    """
    change_list = list()
    count = 0
    for day in reversed(list(df_work_day['cal_date'].tail(day_range))):
        end_t = day
        all_index_end = df_all_day[df_all_day['cal_date'] == end_t].index.tolist()[0]
        #all_date = df_all_day['cal_date'].iat[all_index_num]
        start_t = df_all_day['cal_date'].iat[all_index_end - period]
        #all_index_start = df_all_day[df_all_day['cal_date'] == start_t].index.tolist()[0]
        count += 1
        #print(str(count),start_t,end_t,str(all_index_start),str(all_index_end))
        #change_sum = ("%.2f" % df_hist_data[['change']][all_index_start:all_index_end].sum())
        change_sum = ("%.2f" % df_hist_data[(df_hist_data['trade_date']>=str(start_t)) & (df_hist_data['trade_date']<=str(end_t))]['change'].sum())
        print(str(count),start_t,end_t,str(change_sum))
        #cycle_p_change_list.append(cycle_p_change_sum)
        #print(day_time,str(cycle_p_change_sum))
    return(change_list)

if __name__ == "__main__":

    pro = ts.pro_api('token')
    #stock_list = ['000998']
    #stock_code = sys.argv[1]
    stock_code = '000998.SZ'

    #cycle_time = 90
    #day_range = 150
    pre_days = 30
    day_range = 90

    num4days = day_range*2 + pre_days

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)

    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
    #print(df_hist_data)

    day_list = [i for i in range(0,day_range+1)]
    period = 10
    all_day,work_day,df_all_day,df_work_day = get_days(pro,start_day,end_day)
    #print(all_day)
    #print(work_day)
    #change_list = get_change_list(df_hist_data,day_list,period)
    get_change_list(df_hist_data,df_work_day,df_all_day,period,day_range)
