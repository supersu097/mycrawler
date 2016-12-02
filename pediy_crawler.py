#!/usr/bin/env python
# coding=utf-8
# Created by sharp.gan at 2016-11-30
import re
import time
import requests
import argparse
from bs4 import BeautifulSoup


class Crawler():
    url = "http://bbs.pediy.com/forumdisplay.php?f=161&order=desc&page="

    def soup_getter(self, page_num):
        rep_data = requests.get(self.url + str(page_num))
        soup = BeautifulSoup(rep_data.content, 'html5lib')
        return soup

    def page_amount_getter(self):
        return int(self.soup_getter(1).select(
            'div.pagenav td.vbmenu_control')[0].get_text().split(' ')[-2])

    def result_output(self, content, filename):
        print content.encode('utf-8')
        with open(filename, 'a+') as f:
            f.write(content.encode('utf-8') + '\n')

    def all_tagged_thread_getter(self):
        for i in range(1, 1000):
            if i > self.page_amount_getter():
                break
            threads_box = self.soup_getter(i).find_all(id=re.compile('td_threadtitle'))
            for i in threads_box:
                single_thread_box = i.find(id=re.compile('thread_title'))
                single_thread_url = 'http://bbs.pediy.com/showthread.php?' + 't=' + \
                                    single_thread_box.get('href').split('=')[-1]
                self.result_output(single_thread_box.get_text() + '   ' + single_thread_url,
                                   'all.txt')
                # The item in threads_box is a <td> tag. when we need to find
                # the img tag,we must find in its parent tag namely the <tr> tag.
                img_list = i.parent.find_all('img')
                for img in img_list:
                    if img.get('src').split('/')[-1].lstrip() in \
                            ['jhinfo.gif', 'good_3.gif', 'good_2.gif']:
                        # print single_thread_box
                        self.result_output(single_thread_box.get_text() + '   ' + single_thread_url,
                                           'all_tagged.txt')
            time.sleep(3)

    def keywords_filter(self, keyword):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="A crawler for the bbs of pediy's Android security forum,"
                    "also you can modify the url to crawl other forum.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-a', '--all',
        action='store_true',
        help='Get all threads and tagged threads of 优秀,精华 and 关注')

    args = parser.parse_args()
    crawler = Crawler()
    if args.all:
        crawler.all_tagged_thread_getter()
