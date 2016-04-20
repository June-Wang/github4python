#!/usr/bin/env python3.4

import sys
import csv
import sqlalchemy as sa
import mysql.connector

csvin = 'cashflow'
years = range(2012,2016)
seasons = range(1,5)
cells = [(year,season) for year in years for season in seasons]

user = 'stockadmin'
host = 'localhost'
password = 'stock2016'
database = 'stock'
table = csvin

mysql_config = {
'user': user,
'host': host,
'password': password,
'database': database
}

conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()


for year,season in cells:
    print(year,season)
    filename = '../csv/'+str(csvin)+str(year)+'_'+str(season)+'.csv'
    try:
        with open(filename,'rt') as fin:
            cin = csv.DictReader(fin)
            rows = [row for row in cin]
    except FileNotFoundError as msg:
        print(msg)
        sys.exit(1)

    db_field_list = cin.fieldnames[1:]
    
    for row in rows:
        data_value_list = list()
        for field in db_field_list:
            data_value_list.append(row[field])

        db_field_list.extend(['year','season'])
        year_str = str(year)
        season_str = str(season)
        data_value_list.extend([year_str,season_str])
        str_s = ''
        str_s = len(db_field_list)*',%s'

        db_field_str = ','.join(db_field_list)
        
        sql = 'INSERT INTO '+table+' '+ '('+db_field_str+')'+' VALUES '+'('+str_s[1:]+');'
        print(sql)
        #sys.exit(1)
        cursor.execute(sql,data_value_list)

#cursor.close()
