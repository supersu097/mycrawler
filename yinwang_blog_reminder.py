#!/usr/bin/env python3
# coding=utf-8

import os
import requests
from bs4 import BeautifulSoup
from core import helper



def page_source_get():
    try:
        yinwang_blog = 'http://www.yinwang.org/'
        rep_data = requests.get(yinwang_blog).text
        return rep_data

    except requests.exceptions.RequestException:
        helper.logger_getter().error('Network connection error')
        exit(1)


def first_aTag_extract():
    soup = BeautifulSoup(page_source_get(), 'html5lib')
    firstURL = soup.select('ul.list-group li a')[0]
    return firstURL


def firstURL_persistence():
    helper.dir_check(helper.TEMP_DIR)
    with open(helper.TEMP_DIR + '/yinBlog_1stURL.txt', 'w') as f:
        f.write(first_aTag_extract().get('href'))
    helper.logger_getter().info("First init to store the url of the first post!")


def check_new():
    if not os.path.isfile(helper.TEMP_DIR + '/yinBlog_1stURL.txt'):
        firstURL_persistence()
        exit(0)
    with open(helper.TEMP_DIR + '/yinBlog_1stURL.txt') as f:
        # if new first url doesn't equal to the record one, upgrade it first!
        if first_aTag_extract().get('href') != f.readline():
            firstURL_persistence()
            helper.mail_send('垠神发表了新Blog: ' + first_aTag_extract().get_text().strip(),
                             'http://www.yinwang.org' + first_aTag_extract().get('href'))
            helper.logger_getter().info('Yinwang published a new blog!')


if __name__ == '__main__':
    check_new()