#!/usr/bin/env python3

import sys
import re
import os
import datetime
import time
import multiprocessing
import tushare as ts
import pandas as pd

def get_data_list(df,day_list):
    change_sum = 0.0
    count = 0
    data_list = {}
    #for my_date in date_list:
    for date in df.index.values:
        try:
            change_tmp = float(df[df.index == date].p_change[0])
        except:
            change_tmp = 0.0
        change_sum += change_tmp
        count = count +1
        #if count in day_list:
        data_list[count] = change_sum
    return(data_list)

def get_data_grow_list(df,day_list):
    count = 0
    w_count = 0
    data_grow_list = {}
    end_num = day_list[-1]+1
    for date in df.index.values:
        if count < end_num:
            try:
                change = float(df[df.index == date].p_change[0])
            except:
                change = 0
            if change >= 0:
                w_count = w_count +1
            else:
                w_count = w_count -1
            count = count +1
            persent = w_count / count * 100
            data_grow_list[count] = persent
        else:
            break
    #print(data_grow_list)
    return(data_grow_list)

def get_w_data(data_list_dict,days):

    w_data_list = [data_list_dict[i] for i in range(1,days)]

    #print(w_data_list)
    up_data = 0
    down_data = 0
    for data in w_data_list:
        if data >= 0:
            up_data += 1
        else:
            down_data +=1

    w_data = (up_data-down_data)/len(w_data_list)*100
    return(w_data)

def get_day_persent(data_list_dict):
    up2days = 0
    count = 0
    for num in data_list_dict:
        if data_list_dict[num] > 0:
            up2days +=1
        count +=1

    up2persents = float(up2days)/float(len(data_list_dict)) * 100
    down2persents = (100 - up2persents) * -1
    day_persents = int(up2persents + down2persents)
    #print(str(up2days),str(count))
    return(day_persents)

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

def job2weight(stock_code,start_day,end_day,stock_basics,day_list):
    """
    获取单个股票权重 主任务
    """
    #print(day_list)
    #Beginning
    df_hist_data = get_df_hist_data(stock_code,start_day,end_day)

    data_list_dict = get_data_list(df_hist_data,day_list)
    
    #get_day_persent
    persent = get_day_persent(data_list_dict)
    #print(persent)

    w_data_list = [ get_w_data(data_list_dict,i) for i in day_list ]

    data_grow_dict = get_data_grow_list(df_hist_data,day_list)    
    w_data_grow_list = [ get_w_data(data_grow_dict,i) for i in day_list ]

    w_weight_list = [ sum(w_data_list)/len(w_data_list),sum(w_data_grow_list)/len(w_data_grow_list),persent ]
    w_weight = sum(w_weight_list)/len(w_weight_list)
    #print(str(w_weight))

    stock_info = get_stock_info(stock_code,stock_basics,df_hist_data,end_day)
    stock_info.append(str(int(w_weight)))
    #print(stock_info)
    #end
    return(stock_info)

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
    #stock_list = ['000998','600188','601933']
    #print(stock_list)
    #sys.exit(1)

    num4days=160
    day_list = [i for i in range(5,30)]
    #print(day_list)

    now = datetime.date.today()
    end_day = get_end_day(now)
    start_day = get_start_day(now,num4days,day_list)

    stock_basics=get_stock_basics()

    cpus = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cpus)

    results = []
    for stock_code in sorted(stock_list):
        result = pool.apply_async(job2weight,(stock_code,start_day,end_day,stock_basics,day_list))
        results.append(result.get())
        #print(result.get())
    pool.close()
    pool.join()

    #print(results)
    #print(len(results))
    #df_html = pd.DataFrame(results,columns=['日期','代码','名称','价格','行业','权重'])
    df = pd.DataFrame(results,columns=['日期','代码','名称','价格','行业','权重'])
    s = df.style.applymap(color_negative_red,subset=pd.IndexSlice[:, ['权重']]).render()
    #df['new'] = df['权重'].apply(color_negative_red)
    print(s)
    #print(s.to_html(index=False))
