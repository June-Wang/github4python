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

def get_jiejin(stock_code):
#解禁信息
#来源：同花顺
#字段：序号	交易日期	本期解禁数（万股）	最新价	解禁股市值（万元）	占总股本比例（%）	限售股东
	url = 'http://data.10jqka.com.cn/market/xsjj/op/code/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	try:
		table = pd.read_html(resp.text)[0]
		#return(table)
	except:
		return(None)

	if len(table.values)>0:
		return(table)
	else:
		return(None)

def get_yeji(stock_code):
#业绩信息
#来源：同花顺
#字段：序号	报告期	业绩预告类型	业绩预告摘要	净利润变动幅度(%)	上年同期净利润(元)	公告日期
	url = 'http://data.10jqka.com.cn/financial/yjyg/op/code/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	try:
		table = pd.read_html(resp.text)[0]
		#return(table)
	except:
		return(None)

	if len(table.values)>0:
		return(table)
	else:
		return(None)

def get_report(stock_code):
#季度年度报告
#来源：同花顺
#字段：序号	报告期	公告日期 
	url = 'http://data.10jqka.com.cn/financial/yjgg/op/code/'+stock_code+'/ajax/1/'
	resp = requests.get(url)

	try:
		table = pd.read_html(resp.text)[0]
		#return(table)
	except:
		return(None)

	if len(table.values)>0:
		return(table)
	else:
		return(None)

table = get_jiejin('000998')
if table is not None:
	print(table)
#table[table.all().head(10).index[1:]].head(10)
