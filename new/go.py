#!/usr/bin/env python3

import sys,re,os,datetime,time
import tushare as ts
import pandas as pd
import numpy as np
from colorama import Fore, Back, Style
from termcolor import colored, cprint
import urllib.request,multiprocessing
from dateutil import parser

def get_days(pro,start_day,end_day):
    """
    exchange    str Y   交易所 SSE上交所 SZSE深交所
    cal_date    str Y   日历日期
    is_open str Y   是否交易 0休市 1交易
    pretrade_date   str N   上一个交易日
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

def get_df_pct_chg(df,day_range,period):
    pct_chg_index = 'pct_chg_'+ str(period) + 'd'
    pct_chg_list = list()
    for day in range(0,day_range):
        #pct_chg_list.append("%.2f" % df['pct_chg'][day:day+period].sum())
        pct_chg_list.append(df['pct_chg'][day:day+period].sum())
        df_pct_chg = pd.DataFrame(pct_chg_list,columns=[pct_chg_index])
        #print(str(day),str(day+period))
    return(df_pct_chg)

def get_df_hist_data(stock_code,start_day,end_day):
    """
    获取股票的历史数据，参数：股票代码(stock_code)、时间周期(num4days)
    开始时间(start_day)、结束时间(end_day)
    ts_code str 股票代码
    trade_date  str 交易日期
    open    float   开盘价
    high    float   最高价
    low float   最低价
    close   float   收盘价
    pre_close   float   昨收价
    change  float   涨跌额
    pct_chg float   涨跌幅 （未复权，如果是复权请用 通用行情接口 ）
    vol float   成交量 （手）
    amount  float   成交额 （千元）
    """
    try:
        df_hist_data = df = pro.query('daily', ts_code=stock_code, start_date=start_day, end_date=end_day)
    except:
        print('get_hist_data timeout!')
        sys.exit(1)
    return(df_hist_data)

def conv_date(val):
    if len(str(val)) == 8:
        timestamp = parser.parse(val).strftime('%s000000000')
    else:
        timestamp = '0000000000000000000'
    return(timestamp)

def get_weight(val):
    if float(val) > 0:
        weight = 1
    elif float(val) <0:
        weight = -1
    else:
        weight = 0
    return(weight)

if __name__ == "__main__":

    stock_list = ['000803.SZ','000998.SZ','600519.SH','600188.SH','002056.SZ','600354.SH']
    #stock_code = sys.argv[1]
    #stock_list = [stock_code]

    pre_days = 120
    day_range = 180

    num4days = day_range + pre_days

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)

    #pro = ts.pro_api('token')
    ts.set_token('API_TOKEN')
    pro = ts.pro_api('API_TOKEN')
    
    #df['trade_date'] = pd.to_datetime(df['trade_date'])

    for stock_code in stock_list:
        df_hist_data = get_df_hist_data(stock_code,start_day,end_day)

        pool = multiprocessing.Pool(processes=4)
        period_list = [3,5]
        period_list.extend([i for i in range(10,100,10)])
        job_list = list()
        for period in period_list:
            res = pool.apply_async(get_df_pct_chg, (df_hist_data,day_range,period))
            job_list.append(res.get())

        stock_info = df_hist_data[0:day_range]
        job_list.append(stock_info)
        df_pct = pd.concat(job_list, axis=1, sort=False)
        date_list = list(df_pct['trade_date'])

        chg_list = [str('pct_chg_'+ str(i) + 'd') for i in period_list]
        chg_list.extend(['pct_chg'])
        df_w = df_pct[chg_list].applymap(get_weight)
        df_pct['weight'] = df_w.sum(axis=1)/len(df_w.columns)*100
        df_buy = df_pct[(df_pct['weight'] == -70) & (df_pct['pct_chg_90d'] < -20)]
        df_sell =df_pct[(df_pct['weight'] == 70) & (df_pct['pct_chg_90d'] > 20)]
        df_stock = pd.concat([df_buy,df_sell])
        df_stock = df_stock.sort_values(by='trade_date',ascending=False)
        print(df_stock[['trade_date','ts_code','close','weight','pct_chg_90d']].to_csv(index=False))
