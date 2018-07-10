#!/usr/bin/env python3

import csv,datetime,sys
import requests

def make_time_url(frequency):
    #frequency=1
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
        download = s.get(csv_url,stream=True,auth=(user, passwd))
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        data_list = list(cr)
        #for row in data_list:
        #    print(row)
        return(data_list)

if __name__=="__main__":
    graylog_url='http://graylog.server.local:9000/api/search/universal/absolute/export?'
    search_condition='query=nginx_version%3A1.6.x&'
    request_fields='fields=timestamp%2Crequest%2Cresponse%2Cagent%2CTIME&decorate=true'
    frequency=1
    time_url = make_time_url(frequency)
    csv_url = graylog_url+search_condition+time_url+request_fields
    print(csv_url)
    data_list = get_csv_data(csv_url,'admin','Ab2016')
    print(data_list)
