# -*- coding: utf-8 -*-
import re

import requests
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem
import csv


# 取得各种信息
class GetInfo(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                      'like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

    # 和风天气主页https://dev.qweather.com/
    def get_qweather(self):
        # 获取天气数据链接
        url_api_weather = 'https://devapi.qweather.com/v7/weather/'
        url_api_geo = 'https://geoapi.qweather.com/v2/city/'
        url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'
        url_api_air = 'https://devapi.qweather.com/v7/air/now'
        # 个人APIKEY
        KEY = '39736e9a40184e95998d6d6ef9dfae48'
        # 获取天气链接参数
        api_type = '3d'
        city_id = '101301301'  # 北海市
        mykey = '&key=' + KEY
        # 获取天气数据链接
        url = url_api_weather + api_type + '?location=' + city_id + mykey
        response = requests.get(url, headers=self.headers, timeout=30)
        if response.status_code == 200:
            return response.json()
        else:
            return None

    # 取得每日一图和每日一句
    def get_dailysentence(self):
        # 英语每日一句链接
        url = 'http://dict.eudic.net/home/dailysentence/'
        # 开始抓取
        response = requests.get(url, headers=self.headers, timeout=30)
        if response.status_code == 200:
            html = response.text
            sentence = re.search(r'<p class="sect-trans">.*</p>', html).group()[22:-4]
            img_url = re.search(r'<img src="http:.*jpg', html).group()[10:]
            return sentence, img_url
        else:
            return None


my_bot_info = GetInfo()

today_weather = my_bot_info.get_qweather()
textDay = today_weather['daily'][0]['textDay']  # 天气
tempMin = today_weather['daily'][0]['tempMin']  # 最低温度
tempMax = today_weather['daily'][0]['tempMax']  # 最高温度
windDirDay = today_weather['daily'][0]['windDirDay']  # 风向
windScaleDay = today_weather['daily'][0]['windScaleDay']  # 风力

# 定义消息内容 第一行标题，第二行天气，第三行图片链接，第四行每日一句
mkd_msg = '### 今天天气\n' \
          '{textDay} {tempMin} - {tempMax} ℃，{windDirDay} {windScaleDay} 级。 \n\n' \
          '![每日一图](http://WWW.BAIDU.COM)\n' \
          '##### 每日一句： \n' \
    .format(textDay=textDay, tempMin=tempMin, tempMax=tempMax,
            windDirDay=windDirDay, windScaleDay=windScaleDay)
# img=today_img, sentence=today_sentence)
#

KEY = '39736e9a40184e95998d6d6ef9dfae48'
location = '101301301'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         'like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

url_api_indices = 'https://devapi.qweather.com/v7/indices/1d?type=1&location=101301301&key=39736e9a40184e95998d6d6ef9dfae48'

url = url_api_indices + location + '&key=' + KEY
response = requests.get(url_api_indices, headers=headers, timeout=30)
if response.status_code == 200:
    result = response.json()
    text = result['daily'][0]['text']
    print(text)



with open('bots.csv', 'r') as f:
    reader = csv.reader(f)
    bots = list(reader)

webhook = bots[0][0]
secret = bots[0][1]

dingding = DingtalkChatbot(webhook, secret=secret)
dingding.send_text(msg=text)
# dingding.send_markdown(title='今日天气', text=mkd_msg, is_at_all=False)
