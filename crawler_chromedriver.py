# coding = 'utf-8'

from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from user_agent import generate_user_agent
from os.path import join as os_join
from bs4 import BeautifulSoup
import os
import time
import pandas


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

    def process_data(self, page_source):
        soup = BeautifulSoup(page_source, 'lxml')
        company_list = soup.select('ul.item_con_list li')
        data_list = []
        for company in company_list:
            attrs = company.attrs
            company_name = attrs['data-company']
            job_name = attrs['data-positionname']
            job_salary = attrs['data-salary']
            data_list.append(company_name + ',' + job_name + ',' + job_salary)
        return data_list

    def get_next_page_source(self):
        try:
            self.driver.implicitly_wait(5)
            self.driver.set_script_timeout(20)
            self.driver.set_page_load_timeout(25)
            next_page = self.driver.find_elements_by_xpath("//span[@class='pager_next ']")
            next_page[0].click()
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

    @staticmethod
    def save_data(self, data, csv_header):
        table = pandas.DataFrame(data)
        table.to_csv(r'/Users/sharp/Desktop/LaGou.csv', header=csv_header, index=False, mode='a+')

    def save_data_into_csv(self, line_data):
        with open(r'/Users/sharp/Desktop/LaGou.csv', 'a+') as f:
            f.write(line_data+'\n')


url = 'https://www.lagou.com/jobs/list_linux%E8%BF%90%E7%BB%B4?labelWords=&fromSearch=true&suginput='
lagou = Lagou(url)
print('Get page {} source'.format(str(1)))
first_page_source = lagou.get_first_page_source()
first_page_data = lagou.process_data(first_page_source)
lagou.save_data_into_csv('company_name,job_name,job_salary')
for data in first_page_data:
    lagou.save_data_into_csv(data)

for i in range(1, 30):
    print('Get page {} source'.format(str(i+1)))
    next_page_source = lagou.get_next_page_source()
    next_page_data = lagou.process_data(next_page_source)
    for data in first_page_data:
        lagou.save_data_into_csv(data)
    time.sleep(8)
