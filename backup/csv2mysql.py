#!/usr/bin/env python3.4

import sys
import csv
import sqlalchemy as sa
import mysql.connector

#csvin = 'cashflow'
#csvin = 'report'
files = ['cashflow','debtpaying','growth','operation','profit','report']
years = range(2016,2017)
seasons = range(1,2)
cells = [(year,season) for year in years for season in seasons]

conn = sa.create_engine('mysql+mysqlconnector://stockadmin:stock2016@localhost/stock')
#conn = mysql.connector.connect(**mysql_config)
#cursor = conn.cursor()

for csvin in files:
    table = csvin
    for year,season in cells:
        print(year,season,csvin)
        filename = '../csv/'+str(csvin)+str(year)+'_'+str(season)+'.csv'
        try:
            with open(filename,'rt') as fin:
                cin = csv.DictReader(fin)
                rows = [row for row in cin]
        except FileNotFoundError as msg:
            print(msg)
            sys.exit(1)
    
        db_field_list = cin.fieldnames[1:]
    #    print(db_field_list)
        
        for row in rows:
            data_value_list = list()
    
            #marks = ', '.join('?' * len(myDict))
            #qry = "Insert Into Table (%s) Values (%s)" % (qmarks, qmarks)
            #cursor.execute(qry, myDict.keys() + myDict.values())
    
            for field in db_field_list:
                data_value_list.append(row[field])
    
            #db_field_list.extend(['year','season'])
            db_field_list_new = [row for row in db_field_list]
            db_field_list_new.extend(['year','season'])
    #        print(db_field_list_new)
    
            year_str = str(year)
            season_str = str(season)
    
            data_value_list_new = [row for row in data_value_list]
            data_value_list_new.extend([year_str,season_str])
    
            str_s = len(db_field_list_new)*',%s'
            marks = str_s[1:]
            db_field_list_new_str = ', '.join(db_field_list_new)
            data_value_list_new_str = str(data_value_list_new).replace('[', '').replace(']', '')
    
            qry = "Insert Into %s (%s) Values (%s);" % (table,db_field_list_new_str,data_value_list_new_str)
            #print(qry)
            #cursor.execute(qry)
            try:
                conn.execute(qry)
            except:
                continue
    #cursor.close()
