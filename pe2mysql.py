#!/usr/bin/env python3

import sys
import re
import os
import datetime
import time
import tushare as ts
import pandas as pd
import numpy as np
import mysql.connector
from mysql.connector import errorcode

def get_pe_data():
    try:
        df_pe = ts.get_stock_basics()
    except:
        print('get df_data timeout!')
        sys.exit(1)
    return(df_pe)

def con_mysql(user,password,host,database):
    config = {
      'user': user,
      'password': password,
      'host': host,
      'database': database,
      'raise_on_warnings': True,
    }
    
    try:
      cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)
    
    cursor = cnx.cursor()
    return(cursor,cnx)

def main():
    cursor,cnx = con_mysql('pe','pe2018','127.0.0.1','stock')
    
    now = datetime.date.today()
    date_time = now.strftime('%Y-%m-%d')
    index_time = now.strftime('%Y%m%d')
    df_pe = get_pe_data()
    
    add_pe = ("INSERT INTO tbl_pe_day "
                      "(id, date, code, pe) "
                      "VALUES (%(id)s, %(date)s, %(code)s, %(pe)s)")
    
    for code in df_pe.index:
        pe = int(df_pe[df_pe.index == code]['pe'][0])
        index = index_time + code
        data_pe = {
          'id': index,
          'date': date_time,
          'code': code,
          'pe': pe,
        }
    
        cursor.execute(add_pe, data_pe)
    
    cnx.commit()
    cursor.close()
    cnx.close()

if __name__ == '__main__':
    main()
