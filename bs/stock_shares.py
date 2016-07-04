#!/usr/bin/env python3.4

import re
import sys
import os
import requests
import pandas as pd
#from bs4 import BeautifulSoup

stock_code = sys.argv[1]
#url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/600519/ajax/1/'
url = 'http://data.10jqka.com.cn/financial/sgpx/op/code/code/'+stock_code+'/ajax/1/'
resp = requests.get(url)
#bsobj = BeautifulSoup(resp.text,"lxml")
#print(bsobj)
#print(bsobj.text)

table = pd.read_html(resp.text)[0]
print(table[['股票代码','股票简称','股权登记日']])
print(len(table))
