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


def blog_url_extract(url):
    try:
        rep_data = requests.get(url)
        soup = BeautifulSoup(rep_data.text, 'html5lib')
        blogs = soup.select('ul.list-group li a')
        return blogs
    except requests.exceptions.RequestException:
        print(' Got an issue of network that we are not very sure,'
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
            print('The crawler is already running,just wait a second...')
            time.sleep(86400)
            for i in blog_url_extract(yinwang_blog):
                if i.get('href') not in old_url_list:
                    mail_send(i.get_text(), i.get('href'))
            else:
                print('The blog of yinwang do not update on {},'
                      'what the fucking sad!!!'.format(datetime.date.today()))
        except TypeError:
            print('Due to the upstream unknown mistake,just keep ignoring...')


