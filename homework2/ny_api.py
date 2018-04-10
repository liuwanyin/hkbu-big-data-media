# -*-coding:utf-8-*-
import json
import traceback
import sys
import requests


reload(sys)
sys.setdefaultencoding('utf8')


def http_request(url):
    # 解析url
    proxy = {"http": "http://127.0.0.1:8888", "https": "https://127.0.0.1:8888"}

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    docs = None
    try:
        response = requests.get(url, headers=headers)
        print ('code', response.status_code)
        if response.status_code == 200:
            docs = response.json().response['docs']
    except Exception:
        tb = traceback.format_exc()
        print (tb)
        docs = None
    return docs


def create_url(page):
    # 组装url
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    apikey = "33b4e8d0f9d741579f1b11e95f61dce3"
    q = "sexual%20harassment"  # 要查询的字词
    begin_date = "20171001"
    end_date = "20180323"
    page = str(page)          # 页码
    new_url = url + '?' + apikey + '&' + q + '&' + begin_date + '&' + end_date + '&' + page
    return new_url


def save_json_data(data_list):
    # 保存请求到的json数据
    json_data = {"response": {"docs": data_list}}
    try:
        with open("News_York.json", 'w') as dump_f:  # a为追加模式
            json.dump(json_data, dump_f, ensure_ascii=False)
    except Exception:
        tb = traceback.format_exc()
        print (tb)


def main():
    i = 0
    data_list = []
    while i < 168:
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
