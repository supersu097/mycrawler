#!/usr/bin/env python3
# coding=utf-8

import os
from core import html
from core import helper

zealer_tech = 'http://www.zealer.com:8080/list?cp=2'
page_source=html.page_source_get(zealer_tech, pagetype='special')
first_aTag = html.first_a_tag_extract(page_source, 'li.series_item a')

video_href =first_aTag.get('href')
video_url = 'http://www.zealer.com:8080' + video_href
video_title = first_aTag.text.split(' ')[-1]
temp_data= helper.TEMP_DIR + '/zealer_tech.txt'

def check_new():
    if not os.path.isfile(temp_data):
        html.first_url_persistence(video_href, '/zealer_tech.txt')
        helper.logger_getter().info("First init to store the url of the first video!")
        exit(0)
    with open(temp_data) as f:
        # if new first url doesn't equal to the record one, upgrade it first!
        if video_href != f.readline():
            helper.logger_getter().info('Zealer published a new video!')
            helper.logger_getter().info('Renew the first url in the file')
            html.first_url_persistence(video_href, '/zealer_tech.txt')
            helper.mail_send('Zealer发了新视频: ' + video_title, video_url)
        else:
            helper.logger_getter().info('Zealer did not publish any new video yet!')

if __name__ == '__main__':
    check_new()