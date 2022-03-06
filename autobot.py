# -*- coding: utf-8 -*-

import sys
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem
from Eduic.DailySentence import EduicContent
from qWeather.qWeatherAPI import QWeatherApi

# 取得天气信息
# 取得系统传入KEY
qweather_key = sys.argv[3]
# 实例化qWeather
qWeather = weather = QWeatherApi(key=qweather_key)
# 取得天气信息
forcast = qWeather.get_weather_forecast()

# 取得每日图片和每日一句
# 实例化Euic
euic = EduicContent()
# 取得每日内容
sentence = euic.get_daily_content()[0]
# 取得每日图片
image = euic.get_daily_content()[1]
# 编辑要发送的信息
md_message = '### 今天天气  \n  ' \
             '##### {forcast}  \n  ' \
             '![picture]({image})  \n  ' \
             '##### {sentence}  \n  '\
    .format(forcast=forcast, image=image, sentence=sentence)

# 接收系统传入的webhook和secret
pipidou_webhook = sys.argv[1]
pipidou_secret = sys.argv[2]

# 实例化DingtalkChatbot
pipidou = DingtalkChatbot(pipidou_webhook, secret=pipidou_secret)

pipidou.send_text(msg='欢迎使用自动化测试脚本')
pipidou.send_markdown(title="今天天气", text=md_message, is_at_all=False)
