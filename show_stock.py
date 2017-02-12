#!/usr/bin/env python3.4

import sys
import re
import datetime
import time
import multiprocessing
import tushare as ts
import pandas as pd
import colorama
from colorama import Fore, Back, Style
from termcolor import colored, cprint

def get_basics_info(code,basics):
	stock_basics = {}
	name = str(basics[basics.index == code][['name']].values[0][0])
	industry = str(basics[basics.index == code][['industry']].values[0][0]) #行业
	area = str(basics[basics.index == code][['area']].values[0][0]) #区域
	pe = str(basics[basics.index == code][['pe']].values[0][0]) #市盈率
	try:
		pb = str(basics[basics.index == code][['pb']].values[0][0]) #市净率
	except:
		pb = 0.0
	stock_basics[code] = {'name':name,'industry':industry,'area':area,'pe':pe,'pb':pb}
	return(stock_basics[code])

file = 're.list'
fh = open(file)
rows = fh.readlines()
fh.close
stock_list = list()
for code in rows:
	m = re.match("^\d{6}$",code)
	if not m:
		continue
	stock_code = code.replace("\n", "")
	stock_list.append(stock_code)

try:
	stock_basics = ts.get_stock_basics()
except:
	print('get_stock_basics timeout!')
	sys.exit(1)

for code in stock_list:
	stock_basics_dict = {}
	stock_basics_dict[code] = get_basics_info(code,stock_basics)
	print(code+'\t'+stock_basics_dict[code]['name']+'\t'+stock_basics_dict[code]['industry'])
