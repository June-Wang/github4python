#!/usr/bin/env python3.4

from bs4 import BeautifulSoup
import re
import sys
import os
import requests


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
			resp = requests.get(page_url)
		except:
			continue
		bsobj = BeautifulSoup(resp.text,"lxml")
		for page in bsobj.findAll("a",{"title":re.compile("尾页")}):
			if page["href"]:
				number4page = page["href"].split('/')[-1]
				index_pages_list.append([page_text,link,number4page])
			else:
				continue
	return(index_pages_list)

def get_page4post(index_pages_list):
	post_pages_list = list()
	for page_text,link,number4page in index_pages_list:
		for i in range(1,int(number4page)):
			page_url = link+str(i)
			try:
				resp = requests.get(page_url)
			except:
				continue

			bsobj = BeautifulSoup(resp.text,"lxml")
			for page in bsobj.findAll("a",{"href":re.compile("\/post\/")}):
				if not page["href"]:
					continue 
				link = page["href"]
				page_name = page.text
				link_list = [ str(url) for url in link.split('#')]
				if len(link_list) >1 or page_name == '留言建议' or page_name == '查看全文':
					continue
				post_pages_list.append([link,page_name])
	return(post_pages_list)

def download_file(post_pages_list,dst_path):
	for link,page_name in post_pages_list:
		#print(link,page_name)
		try:
			resp = requests.get(link)
		except:
			continue
	
		bsobj = BeautifulSoup(resp.text,"lxml") 
		bstitle = bsobj.find("h1")
		art_title = bstitle.text+'.rar'
		#stat = 0
		for download_url in bsobj.findAll("a",{"rel":"nofollow","title":re.compile("^TXT")}):
			#if stat == 1:
			#	break
	
			dl_url = download_url["href"]
			#try:
			#	r = requests.get(dl_url)
			#except:
			#	print(dl_url+'不可访问')
			#	continue
	
			file_name = art_title
			#print('开始下载：'+file_name)
			#try:
			#	with open(dst_path+'/'+file_name, "wb") as save_file:
			#		save_file.write(r.content)
			#	print(file_name+' 下载完毕')
			#	stat = 1
			#except:
			#	print(dst_path+'/'+file_name+'写入失败')
			#	continue
			print(dl_url,file_name)
			break

if __name__ == "__main__":

	web_site = 'http://www.zxcs8.com/'
	resp = requests.get(web_site)
	bsobj = BeautifulSoup(resp.text,"lxml")
	dst_path = '/tmp'
	
	#print(bsobj)
	index_list = get_web_index(bsobj)
	#print(index_list)
	index_pages_list = get_page4index(index_list)
	#print(index_pages_list)
	post_pages_list = get_page4post(index_pages_list)

	download_file(post_pages_list,dst_path)
