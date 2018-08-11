#!/usr/bin/env python3

import datetime,sys,json,requests,os,re
import pandas as pd

def color_negative(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: green'` for negative
    strings, black otherwise.
    """
    if float(val) < -10:
        color = 'green' 
    elif float(val) >= 10:
        color = 'red' 
    else: 
        color = 'black'
    return 'color: %s' % color

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_date(days):
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days = -1)
    end_time = today + datetime.timedelta(days = -2)
    fordays = -1 - days
    start_time = today + datetime.timedelta(days = fordays)
    return(str(yesterday),str(start_time),str(end_time))

def get_query(accountId,date_list,query_template):
    query_list = list()
    for start_time,end_time in date_list:
        url = url_query + query_template % (start_time,end_time,accountId)
        try:
            r = requests.get(url,timeout=2)
        except requests.exceptions.RequestException as error:
            eprint('accountId:',accountId,'message:',error)
            return(accountId,-1,-1)
            #sys.exit(1)
        json_data = r.json()
        #print(json_data)
        if json_data['message'] != 'OK':
            eprint('accountId:',accountId,'message:',json_data['message'])
            return(accountId,-1,-1)
        queryCount = json_data['data']['queryCount']
        query_list.append(queryCount)
    
    query = query_list[0]
    avg_query = query_list[1]/days
    return(accountId,query,avg_query)

def get_accountId(file):
    if not os.path.isfile(file):
        eprint(file,'not found!')
        sys.exit(1)

    with open(file,"r") as fh:
        rows = fh.readlines()
    #print(rows)

    accountId_list = list()
    for row in rows:
        m = re.match("^\d+$",row)
        if not m:
            continue
        id = row.replace("\n", "")
        accountId_list.append(id)
    #print(accountId)
    return(accountId_list)

if __name__ == "__main__":

    url_query = 'http://1.1.1.1:9090/monitor/queryCount/getQueryCount?'
    query_template = """startDate=%s&endDate=%s&serviceCategory=CHECK&accountId=%s"""
    
    days=7
    yesterday,start_time,end_time = get_date(days)
    date_list = [[yesterday,yesterday],[start_time,end_time]]
    
    try:
        file = sys.argv[1]
    except:
        eprint('accountId list not found!')
        sys.exit(1)
    
    accountId_list = get_accountId(file)
    query_data = list()
    #accountId = '3170330'
    persent = 0.0
    for accountId in accountId_list:
        accountId,query,avg_query = get_query(accountId,date_list,query_template)
        #print(accountId,str(query),str(avg_query))
        if avg_query == 0:
            persent = int(query * 100)
        elif query == -1:
            persent = 0
        else:
            persent = int((query-avg_query) / avg_query * 100)
        query_data.append([accountId,query,("%.2f" % avg_query),persent])
        #print(accountId,str(query),str(avg_query),str(persent))
    #print(query_data)
    df = pd.DataFrame(query_data,columns=['accountId','count','avg(7d)','ratio'])
    df.index = df.index + 1
    html = df.style.set_properties(**{'background-color': '#D2D8F9',
                           'color': '#000000',
                           'border-color': 'white'}).applymap(color_negative,subset=pd.IndexSlice[:, ['ratio']]).render()
    print(html)
