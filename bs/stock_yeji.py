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

	#url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/'+stock_code+'/ajax/1/'
	url = 'http://data.10jqka.com.cn/financial/yjyg/op/code/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	try:
		table = pd.read_html(resp.text)[0]
	except:
		return()
	try:
		yeji = table[['业绩预告类型']].values
	except:
		return()
	#for item in yeji:
	
	sum = len(yeji)
	if sum ==0:
		return()
	up_num = list(yeji).count('业绩大幅上升')
	persent = up_num/sum *100
		
	#if str(yeji) == '业绩大幅上升':
	if persent >= 80 and sum >3:
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
