#!/usr/bin/env python3.4

import re
import sys
import os
import requests
import pandas as pd
import tushare as ts
import multiprocessing
#from bs4 import BeautifulSoup

def do_it(stock_code,stock_basics):

	url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	table = pd.read_html(resp.text)[0]
	num = len(table)
	if num >= 16:
		name = stock_basics[stock_basics.index == stock_code]['name'].values[0]
		industry = stock_basics[stock_basics.index == stock_code]['industry'].values[0]
		print(str(stock_code)+'\t'+name+'\t'+industry)

try:
	stock_basics = ts.get_stock_basics()
except:
	print('timeout!')
	sys.exit(1)

stock_list = stock_basics.index.values

#pool = multiprocessing.Pool(processes=3)
for stock_code in sorted(stock_list):
	do_it(stock_code,stock_basics)
#	pool.apply_async(do_it, (stock_code,stock_basics))
#	pool.close()
#	pool.join()
