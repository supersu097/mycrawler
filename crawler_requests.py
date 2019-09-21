# coding = 'utf-8'
import time
import pandas
import random
import requests


def get_data(url, form, header):
    data = requests.post(url, data=form, headers=header).json()
    content = data['content']['positionResult']['result']
    return content


def get_dict(data):
    for i in range(15):
        info = {
            'positionName': data[i]['positionName'],
            'companyShortName': data[i]['companyShortName'],
            'salary': data[i]['salary'],
            'createTime': data[i]['createTime']}
        data[i] = info
    return data


def save_data(data, csv_header):
    table = pandas.DataFrame(data)
    table.to_csv(r'/Users/sharp/Desktop/LaGou.csv', header=csv_header, index=False, mode='a+')


def main():
    header = {
        'Accept': "application / json, text / javascript, * / *; q = 0.01",
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_linux%E8%BF%90%E7%BB%B4?labelWords=&fromSearch=true&suginput=',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
    }
    url = "https://www.lagou.com/jobs/positionAjax.json?" \
          "city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false"
    start_page = 1
    while start_page < 26:
        for page_num in range(start_page, start_page + 5):
            if page_num == 1:
                is_first = 'true'
                csv_header_flag = True
            else:
                is_first = 'false'
                csv_header_flag = False
            form_post = {'first': is_first, 'kd': 'linux运维', 'pn': str(page_num)}
            save_data(get_dict(get_data(url, form=form_post, header=header)))
            print('page: ' + str(page_num))
        start_page += 5
        time.sleep(random.randint(10, 30))


if __name__ == '__main__':
    main()
