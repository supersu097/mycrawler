#!/usr/bin/env python3
# coding=utf-8

import os
import logging
import smtplib
from email.mime.text import MIMEText
from core import config

CURR_PATH = os.path.abspath('.')
TEMP_DIR = CURR_PATH + '/' + 'tmp'

def dir_check(dir):
    if not os.path.isdir(dir):
        os.mkdir(dir)

def mail_send(subject, mail_body):
    host = 'smtp.126.com'
    port = 25
    msg = MIMEText(mail_body, 'plain', 'utf-8')
    msg['Subject'] = subject
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
