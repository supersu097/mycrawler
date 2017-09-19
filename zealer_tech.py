#!/usr/bin/env python3
# coding=utf-8

import os

from bs4 import BeautifulSoup

from core import helper
from core import html

zealer_tech = 'http://www.zealer.com:8080/list?cp=2'
page_source=html.page_source_get(zealer_tech, pagetype='special')
soup = BeautifulSoup(page_source, 'html5lib')
videos_aTags = soup.select('li.series_item a')
temp_data= helper.TEMP_DIR + '/zealer_tech.txt'


def data_persistence():
    with open(temp_data, 'w') as f:
        for i in videos_aTags:
            f.write(i.get('href') + '\n')


def check_new():

    with open(temp_data) as f:
        old_hrefs_list = [i.split()[0] for i in f.readlines()]

    new_videos = [i for i in videos_aTags if i.get('href') not in old_hrefs_list]
    if len(new_videos) == 0:
        helper.logger_getter().info('Zealer did not publish any new video yet!')
    else:
        msg_content='Zealer published new video!'
        helper.logger_getter().info(msg_content)
        helper.mail_send(helper.date_getter() +'  ' + msg_content,msg_content)
        helper.logger_getter().info("Renew the videos' href in the file")
        data_persistence()




if __name__ == '__main__':
    if not os.path.isfile(temp_data):
        helper.logger_getter().info("First init to store all videos' href!")
        data_persistence()
        exit(0)
    check_new()