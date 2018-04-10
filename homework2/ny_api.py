# -*-coding:utf-8-*-
import json
import traceback
import sys
import requests

reload(sys)
sys.setdefaultencoding('utf8')


def http_request(url):
    # 解析url

    headers = {'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit / 537.36 (KHTML, like Gecko) Chrome / 65.0.3325.181 Safari / 537.36'}

    docs = None
    try:
        response = requests.get(url, headers=headers)
        print ('code', response.status_code)
        if response.status_code == 200:
            docs = response.json()['response']['docs']
    except Exception:
        tb = traceback.format_exc()
        print (tb)
        docs = None
    return docs


def create_url(page):
    # 组装url
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json?apikey=33b4e8d0f9d741579f1b11e95f61dce3&q=sexual%20harassment&begin_date=20180102&end_date=20180323&sort=oldest&page="
    new_url = url + str(page)
    return new_url


def save_json_data(data_list):
    # 保存请求到的json数据
    json_data = {"response": {"docs": data_list}}
    try:
        with open("News_York.json20180323", 'w') as dump_f:  # a为追加模式
            json.dump(json_data, dump_f, ensure_ascii=False)
    except Exception:
        tb = traceback.format_exc()
        print (tb)


def main():
    i = 0
    data_list = []
    while i < 140:
        i += 1
        url = create_url(i)         # 获取url
        docs = http_request(url)    # 得到一个包含url的列表
        if docs:
            data_list.extend(docs)  # 将两个列表合并
    if data_list:
        save_json_data(data_list)
        print "OK"


if __name__ == '__main__':
    main()
