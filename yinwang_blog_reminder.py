#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import requests
import time
import pprint
import config
import smtplib
from email.mime.text import MIMEText
import datetime

yinwang_blog = 'http://www.yinwang.org/'


def logger_getter():
    import logging
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s -%(message)s",
                                    datefmt='%Y-%m-%d %H:%M')
    file_handler = logging.FileHandler('tmp.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

def blog_url_extract(url):
    try:
        rep_data = requests.get(url)
        soup = BeautifulSoup(rep_data.text, 'html5lib')
        blogs = soup.select('ul.list-group li a')
        return blogs
    except requests.exceptions.RequestException:
        logger_getter().debug(' Got an issue of network that we are not very sure,'
              'just rest a while to wait the network to normal...')
        time.sleep(3600)



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
        try:
            old_url_list = [i.get('href') for i in blog_url_extract(yinwang_blog)]
            logger_getter().debug('The crawler is already running,just wait a second...')
            time.sleep(86400)
            for i in blog_url_extract(yinwang_blog):
                if i.get('href') not in old_url_list:
                    mail_send(i.get_text(), i.get('href'))
            else:
                logger_getter().debug('The blog of yinwang do not update today,'
                                      'what the fucking sad!!!')
        except TypeError:
            logger_getter().debug('Due to the upstream unknown mistake,just keep ignoring...')


