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
    msg['Subject'] = '垠神的新文章：'.decode('utf-8') + subject
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
        time.sleep(86400)
        for i in blog_url_extract():
            if i.get('href') not in old_url_list:
                mail_send(i.get_text(), i.get('href'))
        else:
            logger_getter().debug('The blog of yinwang do not update today,'
                                  'what the fucking sad!!!')
