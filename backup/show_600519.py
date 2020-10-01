#!/usr/bin/env python3

import sys
import re
import os
import datetime
import time
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
        #print("day_index:\t"+str(day)+'\t'+"day_persent["+str(day)+"]"+"\t"+str(day_persent[day]))
        #print(day_persent[day])

    #persent_sum_dict = dict()
    #for i in range(0,len(days_persent_list)):
    #    persent_sum_dict[i] = np.sum(days_persent_list[i][0].astype(np.float))/len(days_persent_list)
    #print(persent_sum_dict)

    return(persent_dict)

def getContent(url):  
    #此函数用于抓取返回403禁止访问的网页 
    #random_header = random.choice(headers)  
    opener=urllib.request.build_opener()
    cookie='v=AkDLYWX1DnGnYPJ1uM1znWOgEcUWySSTxq14l7rRDNvuNe7zYtn0Ixa9SCUI'
    opener.addheaders = [('Cookie', cookie)]
    content = opener.open(url).read()
    url_data = content.decode('gbk')
    return url_data

def get_share(stock_code):

    url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/'+stock_code+'/ajax/1/'

    try:
        resp = getContent(url)
        table = pd.read_html(resp)[0]
    except:
        print('获取配股分红信息失败！')
        year_list = list()
        return(year_list)
    year_list = [ str(year[0]) for year in table[['除权除息日']].values]
    return(year_list)

if __name__ == "__main__":

    stock_code = '600519'

    cycle_time = 30
    day_range = 150

    num4days = day_range*2 + cycle_time

    year_list = get_share(stock_code)
    day_list = [i for i in range(0,day_range+1)]

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days)

    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)
    sh_hist_data = get_df_hist_data('sh',start_day,end_day)

    cycle_p_change_list = get_cycle_p_change_list(df_hist_data,day_list,cycle_time)
    sh_cycle_p_change_list = get_cycle_p_change_list(sh_hist_data,day_list,cycle_time)

    #info_list = np.vstack(cycle_date_list) + np.vstack(cycle_p_change_list)
    #info = pd.Series((cycle_p_change_list),index = cycle_date_list)
    #print(info)
    
    day_list_persent = [3,5,10]
    #day_list_persent = my_list
    cycle_p_change = dict()
    sh_cycle_p_change = dict()
    for day in day_list_persent:
        cycle_p_change[day] = get_cycle_p_change_list(df_hist_data,day_list,day)
        sh_cycle_p_change[day] = get_cycle_p_change_list(sh_hist_data,day_list,day)
        #print(cycle_p_change_list[day])
    #get_persent_sum_dict(df_hist_data,day_list)
    #print(np.sum(list(days_persent_list[0][0])))
    #sys.exit(0)
    
    persent_cycle_list = [30,60,90]
    persent_cycle = dict()
    sh_persent_cycle = dict()
    for cycle in persent_cycle_list:
        persent_cycle[cycle] = get_persent_dict(df_hist_data,day_list,cycle)
        sh_persent_cycle[cycle] = get_persent_dict(sh_hist_data,day_list,cycle)

    for day in day_list:
        #persent = float(cycle_p_change_list[day])+float(p_change_grow_list[day])
        date = df_hist_data.index.values[day]
        price = df_hist_data[['close']].values[day][0]
        yesterday_price = df_hist_data[['close']].values[day+1][0]
        price_wave = (price - yesterday_price)/yesterday_price*100

        sh_price = sh_hist_data[['close']].values[day][0]
        sh_yesterday_price = sh_hist_data[['close']].values[day+1][0]
        sh_price_wave = (price - yesterday_price)/yesterday_price*100

        if str(date) in year_list:
            share_msg = '配股分红'
        else:
            share_msg = ''

        #ma_field = ['ma5','ma10','ma20']
        #ma_list = [ df_hist_data[[field]].values[day][0] for field in ma_field ]
        #ma_msg = 'MA(5/10/20)\t'+'\t'.join([("%.2f" % field) for field in ma_list])
        #print(ma_msg)
        
        cycle_p_change_list = [ float(cycle_p_change[i][day]) for i in day_list_persent ]
        sh_cycle_p_change_list = [ float(sh_cycle_p_change[i][day]) for i in day_list_persent ]

        cycle_p_change_msg = '\t'.join([get_color(str(field)) for field in cycle_p_change_list])
        sh_cycle_p_change_msg = '\t'.join([get_color(str(field)) for field in sh_cycle_p_change_list])

        w_list = [ float(persent_cycle[cycle][day]) for cycle in persent_cycle_list]
        sh_w_list = [ float(sh_persent_cycle[cycle][day]) for cycle in persent_cycle_list]

        w_msg = 'W('+'/'.join(str(i) for i in persent_cycle_list)+')\t'+'\t'.join([ get_color(str(field)) for field in w_list])
        sh_w_msg = 'W('+'/'.join(str(i) for i in persent_cycle_list)+')\t'+'\t'.join([ get_color(str(field)) for field in sh_w_list])

        avg_persent = sum(w_list)/len(w_list)
        sh_avg_persent = sum(sh_w_list)/len(sh_w_list)

        avg_w_msg = 'AVG:\t'+get_color("%.2f" % avg_persent)
        sh_avg_w_msg = 'SH_AVG:\t'+get_color("%.2f" % sh_avg_persent)

        try:
            yesterday_persent = float(persent_cycle[30][day+1])
        except:
            break

        #persent_wave = float(persent_cycle[30][day]) - float(persent_cycle[30][day+1])

        front_msg = date +'\t'+ str(price)
        p_msg = "P(1/"+'/'.join(str(i) for i in day_list_persent)+")\t"+get_color(("%.2f" % float(price_wave)))+'\t'+cycle_p_change_msg
        mid_msg = p_msg+'\t'+w_msg+'\t'+avg_w_msg
        sh_msg = str(sh_price)+'\t'+sh_avg_w_msg
        

        p3,p5,p10 = cycle_p_change_list
        p_change = float(df_hist_data[['p_change']].values[day][0])
        sh_p_change = float(sh_hist_data[['p_change']].values[day][0])
        persent30 = float(persent_cycle[30][day])
        persent60 = float(persent_cycle[60][day])

        #if persent30 == -100 and persent60 == -100:
        if persent30 <= -80:
            f1_msg = Fore.CYAN+front_msg+Style.RESET_ALL
        #elif p10 >=15 and persent30 == 100 and persent60 == 100:
        elif p10 >=15:
            f1_msg = Fore.YELLOW+front_msg+Style.RESET_ALL
        elif p_change >0:
            f1_msg = Fore.RED+front_msg+Style.RESET_ALL
        elif p_change < 0:
            f1_msg = Fore.GREEN+front_msg+Style.RESET_ALL
        else:
            f1_msg = front_msg

        if sh_avg_persent <= -90:
            f2_msg = Fore.CYAN+sh_msg+Style.RESET_ALL
        elif sh_avg_persent == 100:
            f2_msg = Fore.YELLOW+sh_msg+Style.RESET_ALL
        elif sh_p_change >0:
            f2_msg = Fore.RED+sh_msg+Style.RESET_ALL
        elif sh_p_change < 0:
            f2_msg = Fore.GREEN+sh_msg+Style.RESET_ALL
        else:
            f2_msg = sh_msg

        print(f1_msg+'\t'+mid_msg+'\t'+f2_msg+'\t'+share_msg)
