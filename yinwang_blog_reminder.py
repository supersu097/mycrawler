#!/usr/bin/env python
# coding=utf-8

import time
import config
import logging
import smtplib
import requests
from bs4 import BeautifulSoup
from email.mime.text import MIMEText

yinwang_blog = 'http://www.yinwang.org/'


def logger_getter():
    logger = logging.getLogger()
    if not len(logger.handlers):
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s -%(message)s",
                                      datefmt='%Y-%m-%d %H:%M')
        file_handler = logging.FileHandler('record.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


def blog_source_get():
    while True:
        try:
            rep_data = requests.get(yinwang_blog)
            return rep_data
        except requests.exceptions.RequestException:
            logger_getter().debug('Issue of network so that we cannot '
                                  'get the whole page source,wait then try again...')
            time.sleep(1800)


def blog_url_extract():
    soup = BeautifulSoup(blog_source_get().text, 'html5lib')
    blog_url_lists = soup.select('ul.list-group li a')
    return blog_url_lists


def mail_send(subject, mail_body):
    host = 'smtp.126.com'
    port = 25
    msg = MIMEText(mail_body)
    msg['Subject'] = subject
    msg['From'] = config.sender
    msg['To'] = config.receiver
    s = smtplib.SMTP(host, port)
    s.debuglevel = 1
    s.login(config.sender, config.pwd)
    s.sendmail(config.sender, config.receiver, msg.as_string())
    s.quit()


if __name__ == '__main__':
    while True:
        old_url_list = [i.get('href') for i in blog_url_extract()]
        logger_getter().debug('The crawler is already running,just wait for lots of 1s...')
        time.sleep(3)
        new_url_list = blog_url_extract()
        if len(new_url_list) < len(old_url_list):
            logger_getter().debug('Yinwang delete some blog...')
            disappeared_blog = set(old_url_list) - set(new_url_list)
            if len(disappeared_blog) == 1:
                logger_getter().debug('Yinwang deleted a blog...')
                mail_send('垠神删除了博客: '.decode('utf-8') + [_.get_text() for _ in disappeared_blog][0],
                          'Nothing need to be known this time')
            else:
                logger_getter().debug('Yinwang deleted more than one blog...')
                mail_send('垠神删除了不止一篇博客'.decode('utf-8'),
                          '\n'.join([_.get_text() for _ in disappeared_blog]))

        elif len(new_url_list) > len(old_url_list):
            new_blog = set(new_url_list) - set(old_url_list)
            if len(new_url_list) == 1:
                logger_getter().debug('Yinwang published a new blog...')
                mail_send('垠神发表了新博客: '.decode('utf-8') + [_.get_text() for _ in new_blog][0],
                          [_.get('href') for _ in new_blog][0])
            else:
                logger_getter().debug('Yinwang published more than one new blog...')
                mail_send('垠神发表了不止一篇新博客'.decode('utf-8'),
                          '\n'.join([_.get_text() + ': ' + _.get('href') for _ in new_blog]))

        elif len(new_url_list) == len(old_url_list):
            logger_getter().debug('The blog of yinwang do not update today,'
                                  'what the fucking sad!!!')
