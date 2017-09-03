#!/usr/bin/env python3
# coding=utf-8

import os
import requests
from core import helper
from bs4 import BeautifulSoup

yinwang_blog = 'http://www.yinwang.org/'


def blog_source_write(upstream):
    with open('blog_source.html', 'w') as s:
        s.write(upstream)


def blog_source_get():
    try:
        rep_data = requests.get(yinwang_blog).content
        if os.path.isfile('blog_source.html'):
            return rep_data
        else:
            helper.logger_getter().info("It seems that U don't get the "
                                        "blog source yet,and it had pulled one in"
                                        " local filesystem then just quit...")
            blog_source_write(rep_data)
            exit(0)
    except requests.exceptions.RequestException:
        helper.logger_getter().error('Issue of network so that we cannot '
                                     'get the whole page source...')
        exit(1)


def blog_aTag_extract(blog_source_upstream):
    soup = BeautifulSoup(blog_source_upstream, 'html5lib')
    blog_aTag_lists = soup.select('ul.list-group li a')
    return blog_aTag_lists


def berfore_mail_send_check(diff_blog, blog_list_status):
    if len(diff_blog) == 1:
        helper.logger_getter().debug('Yinwang {0} a blog...'.format(blog_list_status))
        helper.mail_send('Yinwang {0} a blog: '.format(blog_list_status) +
                         [_.get_text().strip() for _ in diff_blog][0],
                         [_.get('href') for _ in diff_blog][0])
    else:
        helper.logger_getter().debug(
            'Yinwang {0} more than one blogs...'.format(blog_list_status))
        helper.mail_send('Yinwang {0} more than one blogs'.format(blog_list_status),
                         '\n'.join(
                             [_.get_text().strip() + ':' + _.get('href')
                              for _ in diff_blog]))

    # There is a fucking thing,it should be very very careful to use the
    # functionality of reformating code in Pycharm since you comment some
    # code,coz I found Pycharm will change the the position of the origin
    # code line you commented to a place you don't expect generally its
    # parent code block but for the plugin of Python-mode in vim seem to no
    # longer exist such problem,nice~

    # write new blog source to the local file
    blog_source_write(blog_source_get())


if __name__ == '__main__':
    uniq_new_aTag_list = set(blog_aTag_extract(blog_source_get()))
    uniq_old_aTag_list = set(blog_aTag_extract(open('blog_source.html')))
    if uniq_old_aTag_list == uniq_new_aTag_list:
        helper.logger_getter().debug('Yinwang do not have a new '
                                     'blog to be published yet!')
    else:
        # In this situation, Yinwang deletes and publish same amount of blogs at
        # the same time.
        if len(uniq_old_aTag_list) == len(uniq_new_aTag_list):
            helper.logger_getter().debug('Yinwang deletes and publish same amount of '
                                         'blogs at the same time')
            new_blog = uniq_new_aTag_list - uniq_old_aTag_list
            disappeared_blog = (
                                   uniq_new_aTag_list ^ uniq_old_aTag_list) - new_blog
            berfore_mail_send_check(new_blog, 'published')
            berfore_mail_send_check(disappeared_blog, 'deleted')
        else:
            if len(uniq_new_aTag_list) < len(uniq_old_aTag_list):
                disappeared_blog = uniq_old_aTag_list - uniq_new_aTag_list
                new_blog = (
                               uniq_old_aTag_list ^ uniq_new_aTag_list) - disappeared_blog
                berfore_mail_send_check(disappeared_blog, 'deleted')
                if len(new_blog) != 0:
                    berfore_mail_send_check(new_blog, 'published')

            elif len(uniq_new_aTag_list) > len(uniq_old_aTag_list):
                new_blog = uniq_new_aTag_list - uniq_old_aTag_list
                disappeared_blog = (
                                       uniq_new_aTag_list ^ uniq_old_aTag_list) - new_blog
                berfore_mail_send_check(new_blog, 'published')
                if len(disappeared_blog) != 0:
                    berfore_mail_send_check(disappeared_blog, 'deleted')
