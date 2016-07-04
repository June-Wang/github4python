#!/usr/bin/env python3.4

import re
import sys
import os
import requests
import pandas as pd
import tushare as ts
#from bs4 import BeautifulSoup

try:
	stock_basics = ts.get_stock_basics()
except:
	print('timeout!')
	sys.exit(1)

stock_list = stock_basics.index.values
for stock_code in sorted(stock_list):
#stock_code = sys.argv[1]
	url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	table = pd.read_html(resp.text)[0]
	num = len(table)
	#list = table[['股票代码','股票简称','股权登记日']][table.index == 0].values
	if num >= 16:
		#code,name,date = list[0]
		name = stock_basics[stock_basics.index == stock_code]['name'].values[0]
		print(str(stock_code)+'\t'+name)
	#print(table[['股票代码','股票简称','股权登记日']])
	#print(len(table))
