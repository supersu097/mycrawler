#!/usr/bin/env python3
# coding=utf-8

import os
import re
from bs4 import BeautifulSoup
from core import helper
from core import html
from core import config


page_source = html.page_source_get(config.v2_notification)

soup = BeautifulSoup(page_source, 'html5lib')
entries_list = soup.select('entry')
timestamps_list = soup.select('entry published')
temp_data = helper.TEMP_DIR + '/v2ex_notification.txt'

def data_persistence():
    with open(temp_data, 'w') as f:
        for i in timestamps_list:
            f.write(i.text + '\n')


def check_new():
    f = open(temp_data)
    data = f.readlines()
    f.close()
    old_data_collection=[i.split()[0] for i in data]
    is_updated= False
    for new in entries_list:
        title = new.find('title').text
        # This condition is used to filter it's a comment with contents.
        if new.find('published').text not in old_data_collection and title != '':
            contents = new.find('content').contents
            link = new.find('link').get('href')

            # This maybe indicates a plain comment to you.
            if len(contents) == 1:
                user_content=re.match(r'^\[CDATA\[\s*(.*)\s*\]\]$',contents[0]).group(1)
                helper.mail_send(title, user_content + '\n' + link)
                helper.logger_getter().info('Someone on V2ex has a direct reply 4 you')
                is_updated = True
            else:
                index = 0
                for you in contents:
                    # To avoid list index out of range
                    if you == contents[-1]:
                        break
                    # This condition is used to filter if someone @ you.
                    if '/member/{}'.format(config.v2_username) in you:
                        helper.mail_send(title + ',并且@了你', "@" + contents[index + 1].split('\n')[0] + '\n' + link)
                        helper.logger_getter().info('Someone on V2ex has a reply also @ 4 you')
                        index += 1
                        is_updated = True

    if is_updated:
        data_persistence()
        helper.logger_getter().info('Renew the data file')
    else:
        helper.logger_getter().info('V2ex has no notification 4 you!')


if __name__ == '__main__':
    if not os.path.isfile(temp_data):
        data_persistence()
        helper.logger_getter().info("It's the First to store all the timestamps!")
        exit(0)
    check_new()