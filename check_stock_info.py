#!/usr/bin/env python3.4

import sys
import tushare as ts
import datetime
import getopt

from email.mime.text import MIMEText
from subprocess import Popen, PIPE

def usage():
	print("Usage:%s [-h|-c|-l|-g|-f|-t] [--help|--code <stock>|--less <number>|--greater <number>|--from <mail>|--to <mail>] args...." % sys.argv[0])

#stock_code = sys.argv[1]
#stock_code_p_change = float(sys.argv[2])

try:
	opts, args = getopt.getopt(sys.argv[1:], "hc:l:g:f:t:", ["help", "code=","less=","greater=","from=","to="])
except getopt.GetoptError:
	print("getopt error!")
	usage()
	sys.exit(1)

lower_num = -999999
higher_num = 999999
for opt,arg in opts:
	if opt in ("-h", "--help"):
		usage()
		sys.exit(1)
	elif opt in ("-l", "--less"):
		lower = arg
		try:
			lower_num = float(lower)
		except:
			usage()
			sys.exit(1)
	elif opt in ("-g", "--greater"):
		higher = arg
		try:
			higher_num = float(higher)
		except:
			usage()
			sys.exit(1)
	elif opt in ("-c", "--code"):
		code = str(arg)
	elif opt in ("-f","--from"):
		mail_from = arg
	elif opt in ("-t","--to"):
		mail_to = arg

stock_code = code
try:
	df = ts.get_realtime_quotes(stock_code)
except:
	print('time out!'+'['+stock_code+'] not found!')
	sys.exit(1)

#print(str(lower_num),str(higher_num))
#sys.exit(1)

now = datetime.date.today()
yestoday = now - datetime.timedelta(days=1)

price = float(df.price[0])


#msg = MIMEText("Here is the body of my message")
#msg["From"] = "me@example.com"
#msg["To"] = "you@example.com"
#msg["Subject"] = "This is the subject."
#p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
#p.communicate(msg.as_string())

if price < lower_num or price > higher_num:
	mail_body = "股票代码: "+str(stock_code)+"当前价格: "+str(price)
	msg = MIMEText(mail_body)
	msg["From"] = str(mail_from)
	msg["To"] = str(mail_to)
	msg["Subject"] = "股票消息提醒"
	p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
	#p.communicate(msg.as_string()) #python2
	p.communicate(msg.as_bytes())

