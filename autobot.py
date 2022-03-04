# -*- coding: utf-8 -*-

import base64
import hashlib
import hmac
import json
import re
import time
import urllib.request
import requests
from Eduic.DailySentence import EduicContent
from KEY.dingtalkbot_key import PiPiDou_webhook, PiPiDou_secret
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem

# 定义钉钉机器人
class DingTalkWebHook(object):
    def __init__(self, url=None, secret=None):
        """
        secret: 钉钉机器人加签信息
        url: 钉钉机器人没有加签的hook url
        """
        if secret is not None:
            secret = secret
        else:
            secret = 'secret'
        if url is not None:
            url = url
        else:
            url = 'https://oapi.dingtalk.com/robot/send?access_token=access_token'

        timestamp = round(time.time() * 1000)
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

        self.webhook_url = url + '&timestamp={}&sign={}'.format(timestamp, sign)

    def send_message(self, data):
        headers = {
            'Content-Type': 'application/json',
            'charset': 'utf-8'
        }
        send_data = json.dumps(data)
        send_data = send_data.encode('utf-8')
        request = urllib.request.Request(url=self.webhook_url, headers=headers, data=send_data)

        opener = urllib.request.urlopen(request)
        print(opener.read())


# 取得各种信息
class GetInfor(object):
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


# WebHook地址
webhook = r'https://oapi.dingtalk.com/robot/send?access_token' \
          r'=80da5c52f55d190c732e25b0d222249c2e509a29df36c78d3b389b14d211c724'
# 机器人密钥
secret = r'SECf1d13f27bbceb66a187c37e1a4e422e87e52d7718727f3a548f9b9533b94c3c0'
# 可选：创建机器人勾选“加签”选项时使用
# 初始化机器人小丁
xiaoding = DingTalkWebHook(webhook, secret=secret)

# 取得天气信息
dinginfo = GetInfor()
today_weather = dinginfo.get_qweather()

textDay = today_weather['daily'][0]['textDay']  # 天气
tempMin = today_weather['daily'][0]['tempMin']  # 最低温度
tempMax = today_weather['daily'][0]['tempMax']  # 最高温度
windDirDay = today_weather['daily'][0]['windDirDay']  # 风向
windScaleDay = today_weather['daily'][0]['windScaleDay']  # 风力

# 取得今日句子
today_sentence = dinginfo.get_dailysentence()[0]
# 取得今日图片链接
today_img = dinginfo.get_dailysentence()[1]

# 定义消息内容 第一行标题，第二行天气，第三行图片链接，第四行每日一句
mkd_msg = '### 今天天气\n' \
          '{textDay} {tempMin} - {tempMax} ℃，{windDirDay} {windScaleDay} 级。 \n\n' \
          '![每日一图]({img})\n' \
          '##### 每日一句：{sentence} \n' \
    .format(textDay=textDay, tempMin=tempMin, tempMax=tempMax,
            windDirDay=windDirDay, windScaleDay=windScaleDay,
            img=today_img, sentence=today_sentence)

mkd = {
    'msgtype': 'markdown',
    'markdown': {
        'title': 'Hello, world!',
        'text': today_sentence,
    },
    'at': {
        'atMobiles': [
            '17777909650'
        ],
        'isAtAll': False
    }
}

# 发送信息
xiaoding.send_message(mkd)

if __name__ == '__main__':
    my_secret = 'SECf1d13f27bbceb66a187c37e1a4e422e87e52d7718727f3a548f9b9533b94c3c0'
    my_url = 'https://oapi.dingtalk.com/robot/send?access_token' \
             '=80da5c52f55d190c732e25b0d222249c2e509a29df36c78d3b389b14d211c724'

    my_makedown = {
        'msgtype': 'markdown',
        'markdown': {
            'title': 'Hello, world!',
            'text': '#### 测试消息1820\n'
        },
        'at': {
            'atMobiles': [
                '17777909650'
            ],
            'isAtAll': False
        }
    }

    # webhook = sys.argv[1]
    # secret = sys.argv[2]

    ding = DingTalkWebHook(secret=my_secret, url=my_url)
    ding.send_message(my_makedown)
    # autoding = DingTalkWebHook(url=webhook, secret=secret)
    # autoding.send_message(mkd_msg)

# 实例化Euic
euic = EduicContent()
# 取得每日内容
sentence = euic.get_daily_content()[0]
# 取得每日图片
image = euic.get_daily_content()[1]

md_message = '### 今天天气  \n  ' \
             '![picture]({image})   \n  ' \
             '##### 每日一句：{sentence}  \n  '\
    .format(image=image, sentence=sentence)


# 实例化DingtalkChatbot
pipidou = DingtalkChatbot(PiPiDou_webhook, secret=PiPiDou_secret)

pipidou.send_text(msg='欢迎使用自动化测试脚本')
pipidou.send_markdown(title="每日一句", text=md_message, is_at_all=False)
