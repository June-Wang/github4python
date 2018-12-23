#!/usr/bin/env python3

import sys
import datetime
import time
import tushare as ts
from influxdb import InfluxDBClient

def get_day_all():
    try:
        #print('Get Day All...')
        df = ts.get_today_all()
    except:
        print('ts.get_today_all failed.')
        sys.exit(1)
    return(df)

def get_json(date_time,persent):
    now = date_time
    number = persent
    json_body = [
        {
            "measurement": "overview_stock",
            "tags": {
                "host": "localhost",
                "region": "home"
            },
            "time": now,
            "fields": {
                "value": number
            }
        }
    ]
    return(json_body)

def json_to_influx(json_body):
    user = 'root'
    password = 'root'
    dbname = 'stock'
    dbuser = 'stock_admin'
    dbuser_password = 'Ab2016'
    try:
        client = InfluxDBClient('localhost', 8086, user, password, dbname)
    except:
        print('date to fluxdb failed!')
        sys.exit(1)
    #client.create_database('stock')
    client.write_points(json_body)

def main():
    
    now = datetime.datetime.now()
    start = now.replace(hour = 9,minute = 45,second = 0)
    end = now.replace(hour = 15,minute = 00,second = 0)
    if now < start or now > end:
        print('Not 9:45-15:00!')
        sys.exit(1)  

    #date_time = now.strftime('%Y-%m-%d %H:%M:%S')
    current_time = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    #print(get_json(current_time,-74))
    df = get_day_all()

    #data = list()    
    persent_all = 0
    for persent in df.changepercent.values:
        if persent > 0:
            persent_all +=1
        else:
            persent_all -=1

    number_of_stock = len(df.changepercent.values)
    persent = int(float(persent_all)/float(number_of_stock)*100)
    json_to_influx(get_json(current_time,persent))

if __name__ == '__main__':
    main()
