#!/usr/bin/env python3
# coding=utf-8

import argparse
import os

from core import helper
from core import html

yinwang_blog = 'http://www.yinwang.org/'
page_source = html.page_source_get(yinwang_blog)
first_aTag = html.first_a_tag_extract(page_source, 'ul.list-group li a')


def check_new(option):
    if not os.path.isfile(helper.TEMP_DIR + '/yinBlog.txt'):
        html.first_url_persistence(first_aTag.get('href'), '/yinBlog.txt')
        helper.logger_getter().info("First init to store the url of the first post!")
        exit(0)
    with open(helper.TEMP_DIR + '/yinBlog.txt') as f:
        # if new first url doesn't equal to the record one, upgrade it first!
        if first_aTag.get('href') != f.readline():
            helper.logger_getter().info('Yinwang published a new blog!')
            helper.logger_getter().info('Renew the first url in the file')
            html.first_url_persistence(first_aTag.get('href'), '/yinBlog.txt')
            blog_url = 'http://www.yinwang.org' + first_aTag.get('href')
            blog_title = first_aTag.get_text().strip()
            helper.mail_send('垠神发表了新Blog: ' + blog_title, blog_url)

            # begin making screenshot
            helper.dir_check(helper.CURR_PATH + '/tmp/yinblog_back')
            html.make_screenshot(blog_url, helper.CURR_PATH + '/yinblog_back/' + blog_title + '.png')


            # decide whether push the screenshot to github repo or not
            if option:
                os.system('git add .')
                os.system("git commit -m 'backup yinwang blog'")
                os.system('git push origin master')

        else:
            helper.logger_getter().info('Yin did not publish any blog yet!')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Help you push the screenshot to the folk of ur own repo.')
    parser.add_argument(
        '-p', '--push',
        action='store_true',
    help = 'Decide whether push the screenshot to github repo or not!')
    args = parser.parse_args()

    check_new(args.push)