#!/usr/bin/env python
# coding=utf-8
# Created by sharp.gan at 2016-11-30
import re
import time
import requests
import argparse
from bs4 import BeautifulSoup

class Crawler():
	url="http://bbs.pediy.com/forumdisplay.php?f=161&order=desc&page="
	def soup_getter(self,page_num):
		rep_data=requests.get(self.url + str(page_num))
		soup=BeautifulSoup(rep_data.content,'html5lib')
		return soup
	def page_amount_getter(self):
		return int(self.soup_getter(1).select('div.pagenav \
								td.vbmenu_control')[0].get_text().split(' ')[-2])
	def result_output(self,content,filename):
		print content
		with open(filename,'a+') as f:
			f.write(content.encode('utf-8') + '\n')

	def all_tagged_thread_getter(self):
		for i in range(1,1000):
			if i > self.page_amount_getter():
				break
			threads_box=self.soup_getter(i).find_all(id=re.compile('td_threadtitle'))
			for i in threads_box:
				# The item in threads_box is a <td> tag. when we need to find
				# the img tag,we must find in its parent tag namely the <tr> tag.
				img_list=i.parent.find_all('img')
				for img in img_list:
					if img.get('src').split('/')[-1].lstrip() in ['jhinfo.gif','good_3.gif','good_2.gif']:
                        single_thread_box=i.find(id=re.compile('thread_title')
						self.result_output(single_thread_box.get_text() + '   '
                         + single_thread_box.get('href'),'all_tagged.txt')
			time.sleep(3)

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description="A crawler for the bbs of pediy's Android security forum," 
		"also you can modify the url to crawl other forum.") 
	parser.add_argument(
		'-a', '--all_tagged',
		action='store_true',
		help='Get all tagged threads of 优秀,精华 and 关注')
	args = parser.parse_args()
	crawler=Crawler()
	if args.all_tagged:
		crawler.all_tagged_thread_getter()

