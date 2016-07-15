#!/usr/bin/env python3.4

import re
import sys
import os
import time
import requests
import pandas as pd
import tushare as ts
import multiprocessing
#from bs4 import BeautifulSoup

def do_it(stock_code,stock_basics):

	url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	try:
		table = pd.read_html(resp.text)[0]
	except:
		return()
	year_list = [ str(year[0]).split("-")[0] for year in table[['预案公布日']].values]
	local_year = time.strftime("%Y", time.localtime())

	count = 0
	num = len(year_list)
	get_year_list = [str(int(local_year) - i) for i in range(num-1)]
	for year in year_list:
		if year in get_year_list:
			count +=1
	if count == num and num>0:
	#if local_year in year_list:
		name = stock_basics[stock_basics.index == stock_code]['name'].values[0]
		industry = stock_basics[stock_basics.index == stock_code]['industry'].values[0]
		print(str(stock_code)+'\t'+name+'\t'+industry)

try:
	stock_basics = ts.get_stock_basics()
except:
	print('timeout!')
	sys.exit(1)

stock_list = stock_basics.index.values

for stock_code in sorted(stock_list):
	do_it(stock_code,stock_basics)
