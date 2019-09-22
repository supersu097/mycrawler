# coding = 'utf-8'
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from user_agent import generate_user_agent
from os.path import join as os_join
from bs4 import BeautifulSoup
import os
import time


class Lagou(object):
    CURR_PATH = os.path.abspath('.')
    CHROME_DRIVER_PATH: str = os_join(CURR_PATH, 'chromedriver_mac')

    def __init__(self, initial_url: str):
        from selenium.webdriver.chrome.options import Options as ChromeOptions
        self.initial_url: str = initial_url
        options: ChromeOptions = ChromeOptions()
        # options.add_argument('headless')
        custom_ua: str = generate_user_agent(os='win')
        options.add_argument('user-agent=' + custom_ua)
        self.driver = ChromeDriver(executable_path=self.CHROME_DRIVER_PATH,
                                   chrome_options=options)

    def get_first_page_source(self):
        try:
            self.driver.implicitly_wait(5)
            self.driver.set_script_timeout(20)
            self.driver.set_page_load_timeout(25)
            self.driver.get(self.initial_url)
            page_source: str = self.driver.page_source
            return page_source
        except KeyboardInterrupt:
            self.driver.quit()
            print('The exception of KeyboardInterrupt '
                  'detected and the chrome driver has quited.')
        except Exception as e:
            print(str(e))
            self.driver.quit()
            exit(1)


def page_parser():
    soup = BeautifulSoup(get_page_source(), 'lxml')
    item_list = soup.select("div.job-list ul li")
    for item in item_list:
        job_title = item.select_one("div.job-title").get_text()
        company_name = item.select_one("h3.name a").get_text().strip()
        job_salary = item.select_one("span.red").get_text()
        print({'job_title': job_title,
               'company_name': company_name,
               'job_salary': job_salary})


page_parser()
