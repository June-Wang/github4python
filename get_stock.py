import requests
url = 'http://hq.sinajs.cn/'
#code = 'sh600486,sh601003,sh601001,sz000998'
code = 'sz000998'
url_req = requests.get(url+'list='+code)
#info4code = url_req.text.split('"')[1].split(',')
#print(info4code)
for info in url_req.text.split('\n'):
	if info:
		stock_code_str = info.split('=')[0].split('_')[-1]
		stock_code_list = info.split('"')[1].split(',')
		stock_code = stock_code_str #股票代码
		stock_code_00 = stock_code_list[0] #股票名字
		stock_code_01 = stock_code_list[1] #今日开盘价
		stock_code_02 = stock_code_list[2] #昨日收盘价
		stock_code_03 = stock_code_list[3] #当前价格
		stock_code_04 = stock_code_list[4] #今日最高价
		stock_code_05 = stock_code_list[5] #今日最低价
		stock_code_06 = stock_code_list[6] #竞买价，即“买一”报价
		stock_code_07 = stock_code_list[7] #竞卖价，即“卖一”报价
		stock_code_08 = stock_code_list[8] #成交的股票数
		stock_code_09 = stock_code_list[9] #成交金额
		stock_code_10 = stock_code_list[10] #买一 数量
		stock_code_11 = stock_code_list[11] #买一 金额
		stock_code_12 = stock_code_list[12] #买二 数量
		stock_code_13 = stock_code_list[13] #买二 金额
		stock_code_14 = stock_code_list[14] #买三 数量
		stock_code_15 = stock_code_list[15] #买三 金额
		stock_code_16 = stock_code_list[16] #买四 数量
		stock_code_17 = stock_code_list[17] #买四 金额
		stock_code_18 = stock_code_list[18] #买五 数量
		stock_code_19 = stock_code_list[19] #买五 金额
		stock_code_20 = stock_code_list[20] #卖一 数量
		stock_code_21 = stock_code_list[21] #卖一 金额
		stock_code_22 = stock_code_list[22] #卖二 数量
		stock_code_23 = stock_code_list[23] #卖二 金额
		stock_code_24 = stock_code_list[24] #卖三 数量
		stock_code_25 = stock_code_list[25] #卖三 金额
		stock_code_26 = stock_code_list[26] #卖四 数量
		stock_code_27 = stock_code_list[27] #卖四 金额
		stock_code_28 = stock_code_list[28] #卖五 数量
		stock_code_29 = stock_code_list[29] #卖五 金额
		stock_code_30 = stock_code_list[30] #日期
		stock_code_31 = stock_code_list[31] #时间
		print(stock_code_00,stock_code,stock_code_03,stock_code_30,stock_code_31)
