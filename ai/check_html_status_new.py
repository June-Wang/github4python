#!/usr/bin/env python3

import csv,datetime,sys,re,os
import requests,dateparser
import numpy as np
import pandas as pd

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

def make_time_url(frequency):
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=frequency)
    time_from = start_time.strftime('%Y-%m-%d %H:%M:00.000')
    time_to = end_time.strftime('%Y-%m-%d %H:%M:00.000')
    time_url = 'from=' + time_from + '&to=' + time_to + '&'
    time_url = time_url.replace(" ", "%20")
    time_url = time_url.replace(":", "%3A")
    return(time_url)

def get_csv_data(csv_url,user,passwd):
    with requests.Session() as s:
        try:
            download = s.get(csv_url,stream=True,auth=(user, passwd),timeout=10)
        except requests.exceptions.RequestException as error:
            eprint(error)
            sys.exit(1)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_list = list(cr)
        return(data_list)

def get_rules(file):
    if not os.path.isfile(file):
        eprint(file,'not found!')
        sys.exit(1)

    with open(file,"r") as fh:
        rows = fh.readlines()
    #print(rows)

    rule_list = list()
    for row in rows:
        m = re.match("[^!#|^$].+$",row)
        if not m:
            continue
        line = row.replace("\n", "")
        rule_list.append(line)
    return(rule_list)

def make_url(frequency,streams,fields):
    graylog_url='http://127.0.0.1:9000/api/search/universal/absolute/export?'
    search_condition= 'query=streams%3A'+ streams + '&'
    fields.replace(",", "%2C")
    request_fields='fields=' + fields
    time_url = make_time_url(frequency)
    csv_url = graylog_url + search_condition + time_url + request_fields
    return(csv_url)

def message(url_msg,html_status,status,sum,warning,critical):
    message_template = """%s - html %s status is %s! count=%s/min"""
    rrd_template = """|count=%s;%s;%s;"""
    message = message_template % (status,html_status,status,sum)
    rrd_msg = rrd_template % (sum,warning,critical)
    msg = message + '\n' + url_msg + '\n' + rrd_msg
    return(msg)

if __name__=="__main__":

    streams = sys.argv[1]
    html_status = sys.argv[2]
    warning = int(sys.argv[3])
    critical = int(sys.argv[4])

    frequency = 1
    #frequency = 100

    fields='status,url'
    csv_url = make_url(frequency,streams,fields)
    #print(csv_url)
    data_list = get_csv_data(csv_url,'admin','passwd')
    data = data_list[1:]

    #print(data)
    #line[0] date line[1] status; line[2] url
    status_url_list = list()
    for line in data:
        status_url_list.append([line[1],line[2]])

    df = pd.DataFrame(status_url_list,columns=['status','url'])

    #url_group = df.groupby(['status','url'])['url'].count()
    url_group = df.groupby(['status','url'])['url'].count().reset_index(name='count').sort_values(['count'], ascending=False)
    s = url_group.reset_index(drop=True)
    s.index = s.index + 1
    
    sum = len(data)
    if sum == 0:
        url_msg = ''
    else:
        url_msg = s.to_string()
        #to list
        #url_list = s.values.tolist()

    if sum >= critical:
        print(message(url_msg,html_status,'critical',sum,warning,critical))
        sys.exit(2)
    elif sum >= warning:
        print(message(url_msg,html_status,'warning',sum,warning,critical))
        sys.exit(1)
    else:
        print(message(url_msg,html_status,'ok',sum,warning,critical))
        sys.exit(0)
