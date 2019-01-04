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
    graylog_url='http://172.21.194.178:9000/api/search/universal/absolute/export?'
    search_condition= 'query=streams%3A'+ streams + '&'
    fields.replace(",", "%2C")
    request_fields='fields=' + fields
    time_url = make_time_url(frequency)
    csv_url = graylog_url + search_condition + time_url + request_fields
    return(csv_url)

if __name__=="__main__":

    streams = sys.argv[1]
    warning = int(sys.argv[2])

    frequency = 1

    fields='status,url_max'
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

    df_group = df.groupby(['status','url'])
    result = df_group.size().reset_index(name='counts')
    result_warning = result[result.counts >= warning]
    if len(result_warning) == 0:
        print('Data is empty!')
        sys.exit(1)
    
    s = result_warning.sort_values(by='counts',ascending=False).reset_index(drop=True)
    s.index = s.index + 1
    html = s.style.set_properties(**{'background-color': '#E5E7E9',
                               'color': '#000000',
                               'border-color': 'white','text-align':'left'}).render()
    print(html)
