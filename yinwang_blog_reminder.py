#!/usr/bin/env python3
# coding=utf-8

import argparse
import os
from bs4 import BeautifulSoup
from core import helper
from core import html


def data_persistence():
    with open(temp_file, 'w') as f:
        for i in aTags_list:
            f.write(i.get('href') + '|' + i.get_text() + '\n')


def check_new(option):
    if not os.path.isfile(temp_file):
        helper.logger_getter().info("First init to store the url of all posts!")
        data_persistence()
        exit(0)

    with open(temp_file) as f:
        previous_posts = [i.split('\n')[0] for i in f.readlines()]
    # inside the list of new_posts, there still are the aTag object
    new_posts = [i for i in aTags_list if i.get('href') + '|' + i.get_text() not in previous_posts]

    if len(new_posts) == 0:
        helper.logger_getter().info('Yin did not publish any blog yet!')

    else:
        for i in new_posts:
            msg_content = 'Yin published a new blog'
            blog_url = yinwang_blog + i.get('href')
            blog_title = i.get_text()
            helper.logger_getter().info(msg_content)
            helper.mail_send(helper.date_getter() + '  ' + msg_content + ':' + blog_title, blog_url)
            # helper.dir_check(helper.CURR_PATH + '/yinblog_back')
            # html.make_screenshot(blog_url, helper.CURR_PATH + '/yinblog_back/' + blog_title + '.png')
        data_persistence()

    # decide whether push the screenshot to github repo or not
    # if option:
    #     os.system('git add .')
    #     os.system("git commit -m 'auto backup yinwang"
    #               " blog - {}'".format(helper.date_getter()))
    #     os.system('git push origin master')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Help you push the screenshot to ur folk of this repo.')
    parser.add_argument(
        '-p', '--push',
        action='store_true',
        help='Decide whether push the screenshot to github repo or not!')
    args = parser.parse_args()

    yinwang_blog = 'http://www.yinwang.org'
    temp_file = helper.TEMP_DIR + '/yin_blog.txt'
    page_source = html.page_source_get(yinwang_blog)
    soup = BeautifulSoup(page_source, 'html5lib')
    aTags_list = soup.select('ul.list-group li a')

    check_new(args.push)
