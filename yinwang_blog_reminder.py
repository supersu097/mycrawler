#!/usr/bin/env python
# coding=utf-8

import os
import config
import logging
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

yinwang_blog = 'http://www.yinwang.org/'


def mail_send(subject, mail_body):
    host = 'smtp.126.com'
    port = 25
    msg = MIMEText(mail_body, 'plain', 'utf-8')
    msg['Subject'] = unicode(subject)
    msg['From'] = config.sender
    msg['To'] = config.receiver
    s = smtplib.SMTP(host, port)
    s.debuglevel = 1
    s.login(config.sender, config.pwd)
    s.sendmail(config.sender, config.receiver, msg.as_string())
    s.quit()


def logger_getter():
    logger = logging.getLogger()
    if not len(logger.handlers):
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s -%(message)s",
            datefmt='%Y-%m-%d %H:%M:%S')
        file_handler = logging.FileHandler('record.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


def blog_source_write(upstream):
    with open('blog_source.html', 'w') as s:
        s.write(upstream)


def blog_source_get():
    try:
        rep_data = requests.get(yinwang_blog).content
        if os.path.isfile('blog_source.html'):
            return rep_data
        else:
            logger_getter().debug("It seems that U don't get the blog source yet,just quit...")
            blog_source_write(rep_data)
            exit(0)
    except requests.exceptions.RequestException:
        logger_getter().debug('Issue of network so that we cannot get the whole page source...')
        exit(1)


def blog_aTag_extract(blog_source_upstream):
    soup = BeautifulSoup(blog_source_upstream, 'html5lib')
    blog_aTag_lists = soup.select('ul.list-group li a')
    return blog_aTag_lists


if __name__ == '__main__':
    new_aTag_list = blog_aTag_extract(blog_source_get())
    old_aTag_list = blog_aTag_extract(open('blog_source.html'))

    if len(new_aTag_list) < len(old_aTag_list):
        disappeared_blog = set(old_aTag_list) - set(new_aTag_list)
        if len(disappeared_blog) == 1:
            logger_getter().debug('Yinwang deleted a blog...')
            mail_send('垠神删除了一篇博客: '.decode('utf-8') +
                      [_.get_text() for _ in disappeared_blog][0],
                      [_.get('href') for _ in disappeared_blog][0])
        else:
            logger_getter().debug('Yinwang deleted more than one blog...')
            mail_send('垠神删除了不止一篇博客'.decode('utf-8'),
                      '\n'.join(
                          [_.get_text() + ':' + _.get('href')
                           for _ in disappeared_blog]))
        # write new blog source to the local file
        if True:
            blog_source_write(blog_source_get())

    elif len(new_aTag_list) > len(old_aTag_list):
        new_blog = set(new_aTag_list) - set(old_aTag_list)
        if len(new_blog) == 1:
            logger_getter().debug('Yinwang published a new blog...')
            mail_send('垠神发表了一篇新博客: '.decode('utf-8') +
                      [_.get_text() for _ in new_blog][0],
                      [_.get('href') for _ in new_blog][0])
        else:
            logger_getter().debug('Yinwang published more than one new blog...')
            mail_send(
                '垠神发表了不止一篇新博客'.decode('utf-8'),
                '\n'.join(
                    [_.get_text() + ': ' + _.get('href') for _ in new_blog]))

        # There is a fucking thing,it should be very very careful to use the the functionality of
        # reformating code in Pycharm since you comment some code
        # write new blog source to the local file
        if True:
            blog_source_write(blog_source_get())

    elif len(new_aTag_list) == len(old_aTag_list):
        logger_getter().debug('Yinwang do not have a new blog to be published yet!')
