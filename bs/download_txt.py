#!/usr/bin/env python3.4

from bs4 import BeautifulSoup
import re
import sys
import os
import urllib.request
from urllib.request import urlopen
import requests

web_site = 'http://www.zxcs8.com/'
resp = requests.get(web_site)
bsobj = BeautifulSoup(resp.text,"lxml")
#print(bsobj)
#sys.exit(0)

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
		#print(page_text,url)
		link = url+'/page/'
		page_url = url+'/page/1'
		try:
			#html = urlopen(page_url)
			resp = requests.get(page_url)
		except:
			continue
		bsobj = BeautifulSoup(resp.text,"lxml")
		#print(bsobj)
		for page in bsobj.findAll("a",{"title":re.compile("尾页")}):
			if page["href"]:
				number4page = page["href"].split('/')[-1]
				index_pages_list.append([page_text,link,number4page])
			#print(index_pages_list[-1])
	#print(index_pages_list)
	return(index_pages_list)

def get_page4post(index_pages_list):
	post_pages_list = list()
	for page_text,link,number4page in index_pages_list:
		for i in range(1,int(number4page)):
			page_url = link+str(i)
			print(page_url)
			try:
				#html = urlopen(page_url)
				resp = requests.get(page_url)
			except:
				continue

			bsobj = BeautifulSoup(resp.text,"lxml")
			print(bsobj.findAll("a"))
			for page in bsobj.findAll("a",{"href":re.compile("\/post\/")}):
				#print(page["href"],page.text)
				link = page["href"]
				page_name = page.text
				if page_name == '留言建议':
					continue
				post_pages_list.append([link,page_name])
			return(post_pages_list)
	#	print(page_text,link,number4page)

#print(bsobj)
index_list = get_web_index(bsobj)
#print(index_list)
index_pages_list = get_page4index(index_list)
#print(index_pages_list)
post_pages_list = get_page4post(index_pages_list)

for link,page_name in post_pages_list:
#	if count >10:
		#sys.exit(0)
	#print(link,page_name)
	try:
		#html = urlopen(link)
		resp = requests.get(link)
	except:
		continue

	bsobj = BeautifulSoup(resp.text,"lxml") 
	bstitle = bsobj.find("h1")
	print(bstitle)
	art_title = bstitle.text+'.rar'
	for download_url in bsobj.findAll("a",{"rel":"nofollow","title":re.compile("^TXT")}):
		dl_url = download_url["href"]
		#print(dl_url,art_title)
		try:
		#	dl_file = requests.urlopen(dl_url)
			r = requests.get(dl_url)
		except:
			print(dl_url+'不可访问')
			continue
		dst_path = '/home/wangxj/txt'
		file_name = art_title
		try:
			with open(dst_path+'/'+file_name, "wb") as save_file:
				save_file.write(r.content)
		except:
			print(dst_path+'/'+file_name+'写入失败')
			continue
		break
