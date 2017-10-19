#!/usr/bin/env python3
# coding=utf-8

import os
import time

from bs4 import BeautifulSoup

from core import config
from core import helper
from core import html

page_source = html.page_source_get(config.v2_notification)
soup = BeautifulSoup(page_source, 'html5lib')
timestamps_list = soup.select('entry published')
entries_list=soup.select('entry')
temp_data = helper.TEMP_DIR + '/v2ex_notification.txt'


def data_persistence():
    with open(temp_data, 'w') as f:
        for i in timestamps_list:
            f.write(i.text + '\n')


def check_new():
    with open(temp_data) as f:
        previous_data_format = [i.split('\n')[0] for i in f.readlines()]

    new_notification = [i.text for i in timestamps_list if i.text not in previous_data_format]

    for i in new_notification:
        for j in entries_list:
            if i == j.find('published').text and j.find('title').text == '':
                new_notification.remove(i)

    if len(new_notification) == 0:
        helper.logger_getter().info('V2ex has no notification 4 you!')

    else:
        current_time = time.strftime("%m-%d|%H:%M", time.localtime())
        msg_content = '  V2ex has a new notification for you.'
        helper.mail_send(current_time+msg_content, msg_content + '\n' + '\n'.join(new_notification))
        helper.logger_getter().info(msg_content)
        data_persistence()
        helper.logger_getter().info('Renew the data file')


if __name__ == '__main__':
    if not os.path.isfile(temp_data):
        data_persistence()
        helper.logger_getter().info("First init to store some temp data from v2ex!")
        exit(0)
    check_new()
