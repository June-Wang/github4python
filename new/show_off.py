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
        df_hist_data = pro.query('daily', ts_code=stock_code, start_date=start_day, end_date=end_day)
    except:
        print('get_hist_data timeout!')
        sys.exit(1)
    return(df_hist_data)

def get_df_hist_common(stock_code,start_day,end_day):
    """
名称	类型	必选	描述
ts_code	str	Y	证券代码
api	str	N	pro版api对象，如果初始化了set_token，此参数可以不需要
start_date	str	N	开始日期 (格式：YYYYMMDD，提取分钟数据请用2019-09-01 09:00:00这种格式)
end_date	str	N	结束日期 (格式：YYYYMMDD)
asset	str	Y	资产类别：E股票 I沪深指数 C数字货币 FT期货 FD基金 O期权 CB可转债（v1.2.39），默认E
adj	str	N	复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None
freq	str	Y	数据频度 ：支持分钟(min)/日(D)/周(W)/月(M)K线，其中1min表示1分钟（类推1/5/15/30/60分钟） ，默认D。对于分钟数据有600积分可用户可以试用（每分钟2次），正式权限请在QQ群私信群主或积分管理员。
ma	list	N	均线，支持任意合理int数值。注：均线是动态计算，要设置一定时间范围才能获得相应的均线，比如5日均线，开始和结束日期参数跨度必须要超过5日。目前只支持单一个股票提取均线，即需要输入ts_code参数。
factors	list	N	股票因子（asset='E'有效）支持 tor换手率 vr量比
adjfactor	str	N	复权因子，在复权数据是，如果此参数为True，返回的数据中则带复权因子，默认为False。 该功能从1.2.33版本开始生效
    """
    try:
        df_hist_common = ts.pro_bar(ts_code=stock_code, adj='qfq', start_date=start_day, end_date=end_day)
    except:
        print('get_hist_common timeout!')
        sys.exit(1)
    return(df_hist_common)

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
    if len(val) == 8:
        timestamp = parser.parse(val).strftime('%s000000000')
    else:
        timestamp = '0000000000000000000'
    return(timestamp)

if __name__ == "__main__":

    #pro = ts.pro_api('token')
    #stock_code = sys.argv[1]
    #stock_list = ['000998.SZ','600519.SH','600188.SH','002056.SZ','600354.SH']
    stock_list = ['000803.SZ']
    #stock_code = '000998.SZ'

    #cycle_time = 90
    #day_range = 150
    pre_days = 90
    day_range = 30

    num4days = day_range*2 + pre_days

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)
    
    for stock_code in stock_list:
        #print(start_day,end_day)
        df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
        df_hist_common = get_df_hist_common(stock_code,start_day,end_day)
        #print(df_hist_data)
        day_list = [i for i in range(0,day_range+1)]
        all_day,work_day,df_all_day,df_work_day = get_days(pro,start_day,end_day)
    
        pool = multiprocessing.Pool(processes=4)
        period_list = [5,10,20,30,60,90]
        job_list = list()
        for period in period_list:
            res = pool.apply_async(get_df_pct_chg, (df_hist_data,df_work_day,df_all_day,period,day_range))
            job_list.append(res.get())
    
        stock_info = df_hist_data[['ts_code','trade_date','close','change','pct_chg','vol','amount']][0:day_range]
        job_list.append(stock_info)
        result = pd.concat(job_list, axis=1, sort=False)
        df_pct = result.loc[:,~result.columns.duplicated()]
        date_list = list(df_pct['trade_date'])
        qfq_close_list = list(df_hist_common['close'][0:day_range])
        df_pct = df_pct.assign(timestamp = [conv_date(x) for x in date_list])
        df_pct = df_pct.assign(qfq_close = [x for x in qfq_close_list])
        print(df_pct)
        #print(df_pct.to_csv(index=True))
        #print(df_pct.to_csv(index=False))

"""
trade_date,pct_chg_5d,pct_chg_10d,pct_chg_20d,pct_chg_30d,pct_chg_60d,pct_chg_90d,ts_code,close,change,pct_chg,vol,amount,timestamp
"""
