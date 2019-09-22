# coding = 'utf-8'
import time
import pandas
import random
import requests


def get_data(url, form, header, cookies):
    data = requests.post(url, data=form, headers=header, cookies=cookies).json()
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
        'Host': 'www.lagou.com',

    }
    cookie = {
        'Cookie': "JSESSIONID=ABAAABAAADEAAFI6199BE1A447A4952E35694FAD6DE09E5; WEBTJ-ID=09152019%2C101310-16d32b205f64fe-0a18f4" \
                  "8ceb2615-38607501-1296000-16d32b205f7bef; _ga=GA1.2.262096296.1568513591; user_trace_token=20190915101315-fb" \
                  "a45bfc-790b-4fb1-a6b1-d6bf5a00c63d; index_location_city=%E6%B7%B1%E5%9C%B3; LG_HAS_LOGIN=1; showExpriedIndex=1;" \
                  " showExpriedCompanyHome=1; showExpriedMyPublish=1; privacyPolicyPopup=false; LGUID=20190915181931-4ec2178a-d7a2-" \
                  "11e9-91f7-525400f775ce; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1568542769; TG-TRACK-CODE=search_code; " \
                  "hasDeliver=191; login=false; unick=""; _putrc=""; LG_LOGIN_USER_ID=""; SEARCH_ID=1ad6806fb533480c8c08fbafec04df62;" \
                  " X_HTTP_TOKEN=ee1143fdf9f9b8746661709651029b68de1e6c3d2d; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1569071666;" \
                  " LGRID=20190921211426-bc6cb87b-dc71-11e9-947e-525400f775ce"}
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
            save_data(get_dict(get_data(url, form=form_post, header=header, cookies=cookie)),
                      csv_header=csv_header_flag)
            print('page: ' + str(page_num))
        start_page += 5
        time.sleep(random.randint(10, 30))


if __name__ == '__main__':
    main()
