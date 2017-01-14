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

def get_color(text):
	my_number = float(text)
	if my_number > 0:
		my_text = colored(text, 'red')
	elif my_number < 0:
		my_text = colored(text, 'green')
	else:
		my_text = text
	return(my_text)

try:
	df = ts.get_today_all()
except:
	print('get_today_all timeout!')
	sys.exit(1)

persent_all = 0
for persent in df.changepercent.values:
	if persent > 0:
		persent_all +=1
	if persent < 0:
		persent_all -=1

number_of_stock = len(df.changepercent.values)

now_status = float(persent_all)/float(number_of_stock)
status_str = get_color((".2f" % now_status))

msg = get_color(("%.2f" % float(persent_all)))+"/"+(str(number_of_stock))
print(msg+" = "+status_str)
