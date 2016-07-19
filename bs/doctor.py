#!/usr/bin/env python3.4

import re
import sys
import os
import time
import requests
import pandas as pd
import tushare as ts
import multiprocessing
from bs4 import BeautifulSoup

def get_score(code):

	url = 'http://doctor.10jqka.com.cn/'+code+'/'
	resp = requests.get(url)
	
	bsobj = BeautifulSoup(resp.text,"lxml")
	try:	
		bignum_html = bsobj.findAll("span",{"class":'bignum'})[0]
	except:
		return(0)
	bignum_bs = BeautifulSoup(str(bignum_html),"lxml")
	bignum = bignum_bs.text
	try:
		smallnum_html = bsobj.findAll("span",{"class":'smallnum'})[0]
	except:
		return(0)
	smallnum_bs = BeautifulSoup(str(smallnum_html),"lxml")
	smallnum = smallnum_bs.text
	
	score = float(bignum+smallnum)
	
	#print(str(score))
	return(score)

try:
	stock_basics = ts.get_stock_basics()
except:
	print('timeout!')
	sys.exit(1)

stock_list = stock_basics.index.values

for stock_code in sorted(stock_list):
	score = get_score(stock_code)
	if score >= 6.5:
		name = stock_basics[stock_basics.index == stock_code]['name'].values[0]
		industry = stock_basics[stock_basics.index == stock_code]['industry'].values[0]
		print(("%.1f" % score),str(stock_code)+'\t'+name+'\t'+industry)
