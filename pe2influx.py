#!/usr/bin/env python3

import sys
import datetime
import tushare as ts
from configparser import ConfigParser

def get_pe_data():
    try:
        print('Get Stock Basics...')
        df_pe = ts.get_stock_basics()
    except:
        print('Get Stock Basics failed.')
        sys.exit(1)
    return(df_pe)

def main():
    df_pe = get_pe_data()

    now = datetime.date.today()
    date_time = now.strftime('%Y-%m-%d')
    #index_time = now.strftime('%Y%m%d')

    #data_pe = list()
    for code in df_pe.index:
        #id = index_time + code
        date = str(date_time)
        pe = str(int(df_pe[df_pe.index == code]['pe'][0]))
        #row = (id,date,code,pe)
        #data_pe.append(row)
        print('stock_pe,'+'code='+code+','+'date='+date+' '+'pe='+pe)

if __name__ == '__main__':
    main()
