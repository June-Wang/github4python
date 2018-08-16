#!/usr/bin/env python3

import datetime,sys,json,requests,os,re
import pandas as pd

def color_negative(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: green'` for negative
    strings, black otherwise.
    """
    if float(val) < 0:
        color = 'green' 
    elif float(val) > 0:
        color = 'red' 
    else: 
        color = 'black'
    return 'color: %s' % color

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def get_date(days):
    today = datetime.date.today()
    yesterday = today + datetime.timedelta(days = -1)
    pt1 = yesterday
    end_time = today + datetime.timedelta(days = -2)
    pt2 = end_time
    fordays = -1 - days
    start_time = today + datetime.timedelta(days = fordays)
    return(str(pt1),str(pt2),str(start_time),str(end_time))

def get_query(accountId,date_list,query_template):
    query_list = list()
    for start_time,end_time in date_list:
        url = url_query + query_template % (start_time,end_time,accountId)
        try:
            r = requests.get(url,timeout=2)
        except requests.exceptions.RequestException as error:
            eprint('accountId:',accountId,'message:',error)
            return(-1,-1,-1)
            #sys.exit(1)
        json_data = r.json()
        #print(json_data)
        if json_data['message'] != 'OK':
            eprint('accountId:',accountId,'message:',json_data['message'])
            return(-1,-1,-1)
        queryCount = json_data['data']['queryCount']
        query_list.append(queryCount)
    
    pt1_query = query_list[0]
    pt2_query = query_list[1]
    avg_query = query_list[2]/days
    #print(pt1_query,pt2_query,avg_query)
    return(pt1_query,pt2_query,avg_query)

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

    url_query = 'http://10.10.2.10:8900/monitor/queryCount/getQueryCount?'
    query_template = """startDate=%s&endDate=%s&serviceCategory=IDENTITY_CHECK&accountId=%s"""
    
    days=7
    pt1,pt2,start_time,end_time = get_date(days)
    date_list = [[pt1,pt1],[pt2,pt2],[start_time,end_time]]
    
    try:
        file = sys.argv[1]
    except:
        eprint('accountId list not found!')
        sys.exit(1)
    
    accountId_list = get_accountId(file)
    query_data = list()
    persent = 0.0
    for accountId in accountId_list:
        pt1_query,pt2_query,avg_query = get_query(accountId,date_list,query_template)
        #print(accountId,str(query),str(avg_query))
        if avg_query == 0:
            persent = int(pt1_query * 100)
        elif pt1_query == -1:
            persent = 0
        else:
            persent = int((int(pt1_query) - avg_query) / avg_query * 100)
        query_data.append([accountId,pt1_query,pt2_query,("%.2f" % avg_query),persent])
        #print(accountId,str(query),str(avg_query),str(persent))
    #print(query_data)
    df = pd.DataFrame(query_data,columns=['AccountId','PT1','PT2','AVG(7d)','Ratio'])
    s = df.sort_values(by='PT1',ascending=False).reset_index()
    s.index = s.index + 1
    #print(s)
    #sys.exit(1)
    html = s.style.set_properties(**{'background-color': '#E5E7E9',
                           'color': '#000000',
                           'border-color': 'white'}).applymap(color_negative,subset=pd.IndexSlice[:, ['Ratio']]).render()
    print(html)
