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


def blog_source_get():
    try:
        rep_data = requests.get(yinwang_blog)
        return rep_data
    except requests.exceptions.RequestException:
        logger_getter().debug('Issue of network so that we cannot get the whole page source...')


def blog_aTag_extract():
    if blog_source_get() != None:
        soup = BeautifulSoup(blog_source_get().content, 'html5lib')
        blog_aTag_lists = soup.select('ul.list-group li a')
        return blog_aTag_lists


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


if __name__ == '__main__':
    while True:
        if blog_aTag_extract() != None:
            logger_getter().debug('Crawler is running...')
            old_aTag_list = blog_aTag_extract()
            time.sleep(3600)
            new_aTag_list = blog_aTag_extract()

            if len(new_aTag_list) < len(old_aTag_list):
                # Notice that in this situation,
                # to get the blog which deleted should use the var of old_aTag_list
                disappeared_blog = set(old_aTag_list) - set(new_aTag_list)
                if len(disappeared_blog) == 1:
                    logger_getter().debug('Yinwang deleted a blog...')
                    mail_send('垠神删除了博客: '.decode('utf-8') + [_.get_text() for _ in old_aTag_list][0], '')
                else:
                    logger_getter().debug('Yinwang deleted more than one blog...')
                    mail_send('垠神删除了不止一篇博客'.decode('utf-8'),
                              '\n'.join([_.get_text() for _ in old_aTag_list][0:len(disappeared_blog)]))

            elif len(new_aTag_list) > len(old_aTag_list):
                new_blog = set(new_aTag_list) - set(old_aTag_list)
                # print 'diff:'
                # print new_blog
                if len(new_blog) == 1:
                    logger_getter().debug('Yinwang published a new blog...')
                    mail_send('垠神发表了新博客: '.decode('utf-8') + [_.get_text() for _ in new_aTag_list][0],
                              [_.get('href') for _ in new_aTag_list][0])
                else:
                    logger_getter().debug('Yinwang published more than one new blog...')
                    mail_send('垠神发表了不止一篇新博客'.decode('utf-8'),
                              '\n'.join([_.get_text() + ': ' +
                                         _.get('href') for _ in new_aTag_list[0:len(new_blog)]]))

            elif len(new_aTag_list) == len(old_aTag_list):
                logger_getter().debug('Yinwang do not have a new blog to be published yet!')
        else:
            logger_getter().debug('Wait a moment...')
            time.sleep(1800)
