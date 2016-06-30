#!/usr/bin/env python3.4

from bs4 import BeautifulSoup
import re
from urllib.request import urlopen

web_site = 'http://www.zxcs8.com/'
html = urlopen(web_site)
bsobj = BeautifulSoup(html,"lxml")

def get_web_index(bsobj):
	index_list = list()
	#for page in bsobj.findAll("a",{"href":re.compile("\/tag\/")}):
	for page in bsobj.findAll("a",{"href":re.compile("\/sort\/")}):
		url = page["href"]
		if url:
			if not page.text:
				continue
			page_text = page.text
		index_list.append([page_text,url])
	return(index_list)

def get_page4index(index_list):
	index_pages_list = list()
	for page_text,url in index_list:
		link = url+'/page/'
		page_url = url+'/page/1'
		try:
			html = urlopen(page_url)
		except:
			continue
		bsobj = BeautifulSoup(html,"lxml")
		for page in set(bsobj.findAll("a",{"title":re.compile("尾页")})):
			number4page = page["href"].split('/')[-1]
			index_pages_list.append([page_text,link,number4page])
			#print(index_pages_list[-1])
	return(index_pages_list)

index_pages_list = list()
index_pages_list = get_page4index(get_web_index(bsobj))
for page_text,link,number4page in index_pages_list:
	print(page_text,link,number4page)
