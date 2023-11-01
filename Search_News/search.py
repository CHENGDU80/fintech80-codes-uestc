import requests
from lxml import etree
from lxml import html
import re
import csv
import pandas as pd

def title_content(u):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'
    }
    resp = requests.get(url=u, headers=headers)
    page_content = html.fromstring(resp.content)
    content = ''
    title = ''
    contents = page_content.xpath('//*[@id="content"]/div[2]/article/div/div/div[1]/div/section[1]/div/div/div/div[1]/div/div/div[1]/ul/li//text()')
    if not contents:
        contents = page_content.xpath('//div[@data-test-id="content-container"]/p/text()')
    if not contents:
        contents = page_content.xpath('//div[@data-test-id="content-container"]/div/p/text()')
    pattern = re.compile(r'[\w\s,.\'-]+')
    for cont in contents:
        clean_cont = pattern.findall(cont)
        content += ' '.join(clean_cont)
    match = page_content.xpath('//*[@id="content"]/div[2]/article/div/div/div[1]/div/section[1]/div/div/div/header/div[2]/h1/text()')
    if match:
        title = match[0]
    if not match:
        match_2 = page_content.xpath('//h1[@class="nf_Y s_dS aW_jt aW_jL aW_jR aW_kE aW_kW aW_k1"]/text()')
        if match_2:
            title = match_2[0]
        if not match_2:
            return 'not found', 'not found'
    # print(title)
    # print(content)
    return title, content


def find_information(key_words, pages, period):
    # 占位符输入属性
    url = 'https://seekingalpha.com/api/v3/searches?' \
          'filter[query]={}&filter[type]=headlines&filter[list]=news&' \
          'filter[period]={}&page[size]=20&' \
          'page[number]={}'.format(key_words, period, pages)
    print(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'
    }
    resp = requests.get(url=url, headers=headers)
    print(resp.status_code)
    resp = resp.json()
    articles = resp['headlines']
    url_list = []
    date_list = []
    comment_list = []
    title_list = []
    content_list = []

    for article in articles:
        url = 'https://seekingalpha.com' + article["url"]
        url_list.append(url)
        comment_list.append(article["comments_count"])
        date_list.append(article["date"])

    for url in url_list:
        t, c = title_content(url)
        if t == 'not found':
            # 删除comment_list的最后一个元素
            comment_list.pop()
            # 删除date_list的最后一个元素
            date_list.pop()
            continue
        title_list.append(t)
        content_list.append(c)

    return title_list, content_list, comment_list, date_list


def save_to_csv(title, content, comment, date, key_words, pages, period):
    data = {'title': title, 'content': content, 'comment': comment, 'date': date}
    df = pd.DataFrame(data)

    # 读取 Csv 文件，将数据追加到文件中
    df.to_csv('./data/{}_{}.csv'.format(key_words, period), mode='a', header=True, index=False)

"""Apple Inc. (AAPL) - 

Microsoft Corporation (MSFT) - 微软公司

Amazon.com Inc. (AMZN) - 亚马逊公司，

Alphabet Inc. (GOOGL) - 谷歌母公司，

Facebook, Inc. (FB) - Facebook公司，

Intel Corporation (INTC) - 英特尔公司，

NVIDIA Corporation (NVDA) - NVIDIA公司，专

Netflix, Inc. (NFLX) - 

Tesla, Inc. (TSLA) -

Adobe Inc. (ADBE) -"""
key_list = [
    'Amazon',
    'Alphabet',
    'Intel',
    'NVIDIA',
    'Netflix',
    'Adobe'
]
pages = 10
period = 'week'
t_0 = []
c_0 = []
cm_0 = []
d_0 = []
for key_words in key_list:
    print(key_words)
    for i in range(1, pages + 1):
        t, c, cm, d = find_information(key_words, i, period)
        t_0 += t
        c_0 += c
        cm_0 += cm
        d_0 += d
    save_to_csv(t_0, c_0, cm_0, d_0, key_words, pages, period)

