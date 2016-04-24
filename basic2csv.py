#!/usr/bin/env python3.4

import sys
import time
import tushare as ts

path = '../csv/'
for year in range(2005,2012):
    for season in  range(1,5):
        print(year,season)
        df_profit = ts.get_profit_data(year,season)
        time.sleep(15)
        df_growth = ts.get_growth_data(year,season)
        time.sleep(15)
        df_operation = ts.get_operation_data(year,season)
        time.sleep(15)
        df_debtpaying = ts.get_debtpaying_data(year,season)
        time.sleep(15)
        df_cashflow = ts.get_cashflow_data(year,season)
        time.sleep(15)
        df_report = ts.get_report_data(year,season)
        time.sleep(15)
        filename = path+'profit'+str(year)+'_'+str(season)+'.csv'
        df_profit.to_csv(filename)
        filename = path+'growth'+str(year)+'_'+str(season)+'.csv'
        df_growth.to_csv(filename)
        filename = path+'operation'+str(year)+'_'+str(season)+'.csv'
        df_operation.to_csv(filename)
        filename = path+'debtpaying'+str(year)+'_'+str(season)+'.csv'
        df_debtpaying.to_csv(filename)
        filename = path+'cashflow'+str(year)+'_'+str(season)+'.csv'
        df_cashflow.to_csv(filename)
        filename = path+'report'+str(year)+'_'+str(season)+'.csv'
        df_report.to_csv(filename)
