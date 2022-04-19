# 查询www.gxrc.com的工作信息
# 参考：https://www.gxrc.com/
# -*- coding: utf-8 -*-

import re
from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent


# 根据关键字列表生成re过滤器
def get_pattern(words):
    if words is not None:
        keywords = [word.strip() for word in words.split(',') if word]
        pattern = '|'.join(keywords)
        return re.compile(pattern)
    else:
        return None


# 生成日期和时间
def get_time_str():
    bj_time = datetime.utcnow() + timedelta(hours=8)
    time_str = bj_time.strftime('%Y%m%d%H%M%S')
    today = bj_time.strftime('%Y-%m-%d')
    return time_str, today


class GXRCAPI(object):

    def __init__(self):
        self.url = 'https://s.gxrc.com/sJob?orderType={channel}&page=1'
        self.headers = {'User-Agent': user_agent()}
        self.session = requests.Session()

    # self.category = [
    #     5467, 5468, 5469, 5470, 5471, 5472,
    #     5473, 5474, 5475, 5476, 5477, 5478,
    # ]

    # 获取每个频道的总页数
    def get_total_page(self, channel):
        html = self.get_html(self.url)
        if html:
            result = re.search(r'(pgInfo_last.*?>)(\d{3})(\+?<\/i>)', html).group(2)
            total_page = int(result)
            return total_page
        else:
            return None

    # 生成频道所有链接
    def get_channel_urls(self, channel):
        html = self.get_html(self.url.replace('{channel}', str(channel)))
        if html:
            soup = BeautifulSoup(html, 'lxml')
            channel_urls = soup.select('#channel_' + str(channel) + ' a')
            return [url.get('href') for url in channel_urls]

        total_page = self.get_total_page(channel)
        if total_page:
            urls = [self.url + '&page=' + str(i) for i in range(1, total_page + 1)]
            return urls
        else:
            return None

    # 获取页面html
    def get_html(self, url):
        try:
            response = self.session.get(url, headers=self.headers)
            response.encoding = 'utf-8'
            return response.text
        except Exception as e:
            print(e)
            return None


if __name__ == '__name__':
    gxrc = GXRCAPI()
    page = gxrc.get_total_page(5470)
    print(page)
