#!/usr/bin/env python3
# coding=utf-8

import os

from bs4 import BeautifulSoup

from core import helper
from core import html


def get_first_video_title():
    zealer_tech = 'http://www.zealer.com:8080/list?cp=2'
    page_source = html.page_source_get(zealer_tech, pagetype='special')
    soup = BeautifulSoup(page_source, 'html5lib')
    return soup.select_one('li.series_item a p').get_text().strip()


def data_persistence(content):
    with open(temp_data, 'w') as f:
        f.write(content)


def check_new():
    previous_video_title = open(temp_data).read()
    current_video_title = get_first_video_title()
    if previous_video_title == current_video_title:
        helper.logger_getter().info('Zealer did not publish any new video yet!')
    else:
        msg_content = 'Zealer published new video!'
        helper.logger_getter().info(msg_content)
        helper.mail_send(helper.date_getter() + '  ' + msg_content, current_video_title)
        helper.logger_getter().info("Renew the first video's title in the file.")
        data_persistence(current_video_title)


if __name__ == '__main__':
    temp_data = helper.TEMP_DIR + '/zealer_tech.txt'
    if not os.path.isfile(temp_data):
        helper.logger_getter().info("First init to store the 1st video's title!")
        data_persistence(get_first_video_title())
        exit(0)
    check_new()
