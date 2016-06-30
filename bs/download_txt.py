#!/usr/bin/env python3.4

from bs4 import BeautifulSoup
import re
import sys
import os
import urllib.request
from urllib.request import urlopen
import requests

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

def get_page4post(index_pages_list):
	post_pages_list = list()
	for page_text,link,number4page in index_pages_list:
		for i in range(1,int(number4page)):
			page_url = link+'/'+str(i)
			try:
				html = urlopen(page_url)
			except:
				continue
			bsobj = BeautifulSoup(html,"lxml")
			for page in bsobj.findAll("a",{"href":re.compile("\/post\/")}):
				#print(page["href"],page.text)
				link = page["href"]
				page_name = page.text
				if page_name == '留言建议':
					continue
				post_pages_list.append([link,page_name])
			return(post_pages_list)
	#	print(page_text,link,number4page)

def get_download_url(url):
	'''
	获取跳转后的真实下载链接
	:param url: 页面中的下载链接
	:return: 跳转后的真实下载链接
	'''
	#urllib.parse.unquote(url).decode('gbk','ignore').encode('utf-8','ignore')
	req = urllib.request.Request(url)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
	response = urllib.request.urlopen(req)
	dlurl = response.geturl()	 # 跳转后的真实下载链接
	return(dlurl)

def download_file(dlurl):
	'''
	从真实的下载链接下载文件
	:param dlurl: 真实的下载链接
	:return: 下载后的文件
	'''
	req = urllib.request.Request(dlurl)
	req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko')
	response = urllib.request.urlopen(req)
	return(response.read())

def save_file(dlurl, dlfolder, dlname):
	'''
	把下载后的文件保存到下载目录
	:param dlurl: 真实的下载链接
	:param dlfolder: 下载目录
	:return: None
	'''
	os.chdir(dlfolder)			  # 跳转到下载目录
	#filename = dlurl.split('/')[-1] # 获取下载文件名
	filename = dlname
	dlfile = download_file(dlurl)
	with open(filename, 'wb') as f:
		f.write(dlfile)
		f.close()
	return None

#index_list = list
index_list = get_web_index(bsobj)
#index_pages_list = list()
index_pages_list = get_page4index(index_list)
post_pages_list = get_page4post(index_pages_list)

dlfolder = "/home/wangxj/txt/"
count = 0
for link,page_name in post_pages_list:
	if count >10:
		sys.exit(0)
	#print(link,page_name)
	try:
		html = urlopen(link)
		#html = response.read().decode('utf8',errors='replace') #中文乱码问题
	except:
		continue

	bsobj = BeautifulSoup(html,"lxml") 
	bstitle = bsobj.find("h1")
	print(bstitle)
	art_title = bstitle.text+'.rar'
	for download_url in bsobj.findAll("a",{"rel":"nofollow","title":re.compile("^TXT")}):
		dl_url = download_url["href"]
		print(dl_url,art_title)
		#try:
		dlurl = get_download_url(dl_url)
		#except:
		#	continue
		save_file(dlurl, dlfolder, art_title) 
		break
	count +=1
