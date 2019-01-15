#!/usr/bin/env python3

import sys,re,os,datetime,time
import tushare as ts
import pandas as pd
import numpy as np
from colorama import Fore, Back, Style
from termcolor import colored, cprint
import urllib.request

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

def get_color(text):
    text_f = float(text)
    if text_f > 0:
        text_color = colored(text, 'red')
    elif text_f < 0:
        text_color = colored(text, 'green')
    else:
        text_color = text
    return(text_color)

def get_persent_dict(df_hist_data,day_list,cycle):
    date_list = [i for i in range(1,cycle)]
    #print(len(date_list))
    day_persent = dict()
    days_persent_list = list()
    for date in date_list:
        #print(date)
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

def do_it(code):
    stock_code = code

    cycle_time = 30
    day_range = 150

    num4days = day_range*2 + cycle_time

    #year_list = get_share(stock_code)
    #day_list = [i for i in range(0,day_range+1)]
    day_list = [0]

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)

    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
    sh_hist_data = get_df_hist_data('sh',start_day,end_day)

    cycle_p_change_list = get_cycle_p_change_list(df_hist_data,day_list,cycle_time)
    sh_cycle_p_change_list = get_cycle_p_change_list(sh_hist_data,day_list,cycle_time)

    day_list_persent = [3,5,10]
    #day_list_persent = my_list
    cycle_p_change = dict()
    sh_cycle_p_change = dict()
    for day in day_list_persent:
        cycle_p_change[day] = get_cycle_p_change_list(df_hist_data,day_list,day)
        sh_cycle_p_change[day] = get_cycle_p_change_list(sh_hist_data,day_list,day)
    
    persent_cycle_list = [30,60,90]
    persent_cycle = dict()
    sh_persent_cycle = dict()
    for cycle in persent_cycle_list:
        persent_cycle[cycle] = get_persent_dict(df_hist_data,day_list,cycle)
        sh_persent_cycle[cycle] = get_persent_dict(sh_hist_data,day_list,cycle)

    for day in day_list:
        date = df_hist_data.index.values[day]
        price = df_hist_data[['close']].values[day][0]
        low = df_hist_data[['low']].values[day][0]
        yesterday_price = df_hist_data[['close']].values[day+1][0]
        price_wave = (price - yesterday_price)/yesterday_price*100

        sh_price = sh_hist_data[['close']].values[day][0]
        sh_yesterday_price = sh_hist_data[['close']].values[day+1][0]
        sh_price_wave = (price - yesterday_price)/yesterday_price*100

        share_msg = ''

        #ma_field = ['ma5','ma10','ma20']
        #ma_list = [ df_hist_data[[field]].values[day][0] for field in ma_field ]
        #ma_msg = 'MA(5/10/20)\t'+'\t'.join([("%.2f" % field) for field in ma_list])
        #print(ma_msg)
        
        cycle_p_change_list = [ float(cycle_p_change[i][day]) for i in day_list_persent ]
        sh_cycle_p_change_list = [ float(sh_cycle_p_change[i][day]) for i in day_list_persent ]

        cycle_p_change_msg = '\t'.join([get_color(str(field)) for field in cycle_p_change_list])
        #sh_cycle_p_change_msg = '\t'.join([get_color(str(field)) for field in sh_cycle_p_change_list])

        w_list = [ float(persent_cycle[cycle][day]) for cycle in persent_cycle_list]
        sh_w_list = [ float(sh_persent_cycle[cycle][day]) for cycle in persent_cycle_list]

        #w_msg = 'W('+'/'.join(str(i) for i in persent_cycle_list)+')\t'+'\t'.join([ get_color(str(field)) for field in w_list])
        w_msg = ''
        for i in range(len(persent_cycle_list)):
            w_msg += 'W'+str(persent_cycle_list[i])+'='+str(w_list[i])+','
        #print(w_msg)

        #sh_w_msg = 'W('+'/'.join(str(i) for i in persent_cycle_list)+')\t'+'\t'.join([ get_color(str(field)) for field in sh_w_list])
        #for i in range(len(persent_cycle_list)):
        #    sh_w_msg += 

        p_msg = ''
        count = 0
        for i in (day_list_persent):
            p_msg += 'P'+str(i)+'='+str(cycle_p_change_list[count])+','
            count += 1
        p_msg = 'P1='+ ("%.2f" % float(price_wave)) + ','+p_msg
        #print(p_msg)
        avg_persent = sum(w_list)/len(w_list)
        sh_avg_persent = sum(sh_w_list)/len(sh_w_list)

        #avg_w_msg = 'AVG:\t'+get_color("%.2f" % avg_persent)
        #sh_avg_w_msg = 'SH_AVG:\t'+get_color("%.2f" % sh_avg_persent)

        low_persent = float((low - yesterday_price)/yesterday_price)*100
        #low_persent_msg = 'LOW:\t'+get_color("%.2f" % low_persent)

        #p3,p5,p10 = cycle_p_change_list
        #p_change = float(df_hist_data[['p_change']].values[day][0])
        sh_p_change = float(sh_hist_data[['p_change']].values[day][0])
        #persent30 = float(persent_cycle[30][day])
        #persent60 = float(persent_cycle[60][day])
        #print(p_change)

        #print(f1_msg+'\t'+mid_msg+'\t'+f2_msg+'\t'+share_msg)
        print('stock_cron,'+'code='+stock_code+' '+p_msg+w_msg+'AVG='+("%.2f" % avg_persent)+','+'SH_AVG='+("%.2f" % sh_avg_persent)+','+'LOW='+("%.2f" % low_persent))

if __name__ == "__main__":

    stock_list = ['000998','600519','600188','002056','600354']
    for code in stock_list:
        do_it(code)
