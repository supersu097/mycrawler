#!/usr/bin/env python3
# coding=utf-8

import os
import logging
import smtplib
from email.mime.text import MIMEText
from core import config
import time

CURR_PATH = os.path.abspath('.')
TEMP_DIR = CURR_PATH + '/' + 'tmp'


def date_getter():
    return time.strftime("%m-%d", time.localtime())


def dir_check(user_dir):
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)


def logger_getter():
    logger = logging.getLogger()
    if not len(logger.handlers):
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "%(filename)s - %(asctime)s - %(levelname)s -%(message)s",
            datefmt='%Y-%m-%d %H:%M:%S')
        dir_check(TEMP_DIR)
        file_handler = logging.FileHandler(TEMP_DIR + '/' + 'record.log')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    return logger


def mail_send(subject, mail_body=''):
    try:
        host = 'smtp.126.com'
        port = 25
        msg = MIMEText(mail_body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = config.sender
        msg['To'] = config.receiver
        s = smtplib.SMTP(host, port)
        s.debuglevel = 0
        s.login(config.sender, config.pwd)
        s.sendmail(config.sender, config.receiver, msg.as_string())
        s.quit()
    except smtplib.SMTPException as e:
        logger_getter().error(str(e))
        exit(1)

