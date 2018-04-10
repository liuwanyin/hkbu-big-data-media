# -*-coding:utf-8-*-
from lxml import etree
import requests
import json
import traceback
import sys
import pandas as pd
import re

reload(sys)
sys.setdefaultencoding('utf8')


def get_json_data():
    with open("News_York.json", 'r') as load_f:
        data = json.load(load_f)
        return data


def get_test_html():
    with open("test.html", 'r') as file:
        html = file.read()
        return html


def http_request(url):
    # 解析url
    proxy = {"http": "http://127.0.0.1:8888", "https": "https://127.0.0.1:8888"}

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }

    html = None
    try:
        response = requests.get(url, headers=headers)
        print ('code', response.status_code)
        if response.status_code == 200:
            html = response.text
    except Exception:
        tb = traceback.format_exc()
        print (tb)
        html = None
    return html


def parse_html(html):
    # 解析html
    # html = re.sub(r"’", r"'", html)
    # html = re.sub(r'“|”', r'"', html)
    # 解决编码问题
    table = {ord(f): ord(t) for f, t in zip(
        u'，。！？【】（）％＃＠＆１２３４５６７８９０',
        u',.!?[]()%#@&1234567890')}
    html = html.decode().translate(table)

    # xpath解析html页面
    selector = etree.HTML(html)
    res_list = selector.xpath('//*[@id="story"]/div/div/p//text()')

    if res_list:
        content_list = [str(res) for res in res_list]  # 将解析后的每个content转换成string格式
        content = ''.join(content_list)  # 将content拼接起来
    else:
        content = None
    return content


def save_data(data):
    # 生成csv文件
    df = pd.DataFrame(data, columns=['title', 'time', 'content'])
    csv_name = 'News_York_data.csv'
    df.to_csv(csv_name, index=None, encoding='utf_8_sig')


def main():
    data_dict = get_json_data()
    data = []
    for docs_list in data_dict['response']['docs']:
        title = docs_list['headline']['main']
        time = docs_list['pub_date']
        url = docs_list['web_url']
        html = http_request(url)
        if html:
            content = parse_html(html)
        else:
            content = None
        data.append([title, time, content])
    save_data(data)


if __name__ == '__main__':
    main()
    # html = get_test_html()
    # print parse_html(html)


