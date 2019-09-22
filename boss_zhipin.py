# coding = 'utf-8'

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent
import time


class BossZhipin(object):
    def __init__(self, url, page_num):
        self.url = url
        self.page_num = page_num

    def get_page_source(self):
        common_header = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                                   "image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
                         "accept-encoding": "gzip, deflate, br",
                         "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                         "user-agent": generate_user_agent(os='win')}
        cookie = {'Cookie': "_uab_collina=156859572282842185693821; __g=-; __c=1568554446;"
                            " _bl_uid=nkkv20m5lbg0z6tmdhq0neb2eL4b; __l=r=https%3A%2F%2Fsao."
                            "zhipin.com%2F&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Frecommend&"
                            "friend_source=0&friend_source=0; lastCity=101280600; _uab_collina"
                            "=156914858939269034789901; __zp_stoken__=5c57D15xzkhQxhenoVfQUqnpa"
                            "QyZqJEqTtkZY5iuQsqpEMobrIseo%2F8vzHjNlFY7Lm8nKbM8eHyH3zyskvBjFPMy8g%3D%3D;"
                            " __a=75666192.1569148589..1568554446.5.1.5.5; t=ihzxNowfNoQFYPs; wt=ihzxNowfNoQFYPs"}

        if self.page_num == 1:
            common_header['referer'] = 'https://www.zhipin.com/c101280600/?' \
                                       'query=linux%E8%BF%90%E7%BB%B4&page=2&ka=page-2'
        else:
            common_header['referer'] = "https://www.zhipin.com/c101280600/?' \
                                       'query=linux%E8%BF%90%E7%BB%B4&page={0}&" \
                                       "ka=page-{0}".format(str(page_num - 1))
        response = requests.get(self.url, headers=common_header, cookies=cookie)
        response.encoding = 'utf-8'
        content = response.text
        return content

    def page_parser(self):
        soup = BeautifulSoup(self.get_page_source(), 'lxml')
        item_list = soup.select("div.job-list ul li")
        for item in item_list:
            job_title = item.select_one("div.job-title").get_text()
            company_name = item.select_one("h3.name a").get_text().strip()
            job_salary = item.select_one("span.red").get_text()
            print({'job_title': job_title,
                   'company_name': company_name,
                   'job_salary': job_salary})


for page_num in range(1, 1000):
    print('Get page ' + str(page_num))
    url = "https://www.zhipin.com/c101280600/?query=linux" \
          "%E8%BF%90%E7%BB%B4&page={0}&ka=page-{0}".format(str(page_num))
    boss = BossZhipin(url, page_num)
    boss.page_parser()
    current_page_source = boss.get_page_source()
    current_page_soup = BeautifulSoup(current_page_source, 'lxml')
    if_next_page = current_page_soup.select_one('a.next.disabled')
    if if_next_page:
        break
    time.sleep(8)
