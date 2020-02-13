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

def get_df_pct_chg(df_hist_data,df_work_day,df_all_day,period,day_range):
    """
    生成周期内涨跌幅的值[返回列表]
    """
    pct_chg_list = list()
    count = 0
    for day in reversed(list(df_work_day['cal_date'].tail(day_range))):
        end_t = day
        all_index_end = df_all_day[df_all_day['cal_date'] == end_t].index.tolist()[0]
        start_t = df_all_day['cal_date'].iat[all_index_end - period]
        count += 1
        pct_chg_sum = ("%.2f" % df_hist_data[(df_hist_data['trade_date']>=str(start_t)) & (df_hist_data['trade_date']<=str(end_t))]['pct_chg'].sum())
        pct_chg_list.append([str(day),pct_chg_sum])
        pct_chg_index = 'pct_chg_'+ str(period) + 'd'
        df_pct_chg = pd.DataFrame(pct_chg_list,columns=['trade_date',pct_chg_index])
        #df_pct_chg.set_index('trade_date')
    return(df_pct_chg)

def conv_date(val):
    if len(val) == 4:
        timestamp = parser.parse(val).strftime('%s000000000')
    else:
        timestamp = '0000000000000000000'
    return(timestamp)

if __name__ == "__main__":

    #pro = ts.pro_api('token')
    #stock_code = sys.argv[1]
    stock_list = ['000998.SZ','600519.SH','600188.SH','002056.SZ','600354.SH']
    #stock_code = '000998.SZ'

    #cycle_time = 90
    #day_range = 150
    pre_days = 90
    day_range = 10

    num4days = day_range*2 + pre_days

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)
    
    for stock_code in stock_list:
        #print(start_day,end_day)
        df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
        #print(df_hist_data)
        day_list = [i for i in range(0,day_range+1)]
        all_day,work_day,df_all_day,df_work_day = get_days(pro,start_day,end_day)
    
        pool = multiprocessing.Pool(processes=4)
        period_list = [5,10,20,30,60,90]
        job_list = list()
        for period in period_list:
            res = pool.apply_async(get_df_pct_chg, (df_hist_data,df_work_day,df_all_day,period,day_range))
            job_list.append(res.get())
    
        stock_info = df_hist_data[['trade_date','close','change','pct_chg','vol','amount']][0:day_range]
        #date_str = stock_info['trade_date'][0]
        #print(stock_info)
        job_list.append(stock_info)
        result = pd.concat(job_list, axis=1, sort=False)
        pct = result.loc[:,~result.columns.duplicated()]
        pct_new = pct.applymap(conv_date,subset=pd.IndexSlice[:, ['trade_date']]).render()
        #timestamp = parser.parse(date_str).strftime('%s000000000')
        #msg = 'tushare_pro,stock_code='+stock_code+' '
        #for item in list(pct.columns):
        #    msg += item + '='+ str(pct[item][0])+ ','
        #print(msg[0:-2]+' '+str(timestamp))
        print(pct_new)
    
