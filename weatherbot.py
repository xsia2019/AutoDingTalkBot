# -*- coding: utf-8 -*-
import sys
from dingtalkchatbot.chatbot import DingtalkChatbot
from Eduic.DailySentence import EduicContent
from Lib.qWeatherAPI import QWeatherApi

# 取得天气信息
# 取得系统传入KEY
qweather_key = sys.argv[3]
# qweather_key = ' '
# 实例化qWeather
qWeather = QWeatherApi(qweather_key)
# 取得天气信息
forcast = qWeather.get_weather_forecast()
# 取得生活指数
indices = qWeather.get_my_indices('Beihai')
# 舒适度指数
indice_text = ''
for i in range(len(indices)):
    indice_text += indices[i] + '  \n  '


# 取得每日图片和每日一句
# 实例化Euic
euic = EduicContent()
# 取得每日内容
# sentence = euic.get_daily_content()[0]
# 取得每日图片
image = euic.get_daily_content()[1]
# 编辑要发送的信息
md_message = '#### 北海实时天气  \n  ' \
             '##### {forcast}  \n  ' \
             '![picture]({image})  \n  ' \
    .format(forcast=forcast, image=image, )

indices_message = '#### 北海生活指数  \n  ' \
                  '###### {indices}  \n  ' \
    .format(forcast=forcast, indices=indice_text, )


# 接收系统传入的webhook和secret
bot_webhook = sys.argv[1]
bot_secret = sys.argv[2]
# bot_webhook = ''
# bot_secret = ''

# 实例化DingtalkChatbot
bot = DingtalkChatbot(bot_webhook, secret=bot_secret)

bot.send_markdown(title="北海实时天气", text=md_message, is_at_all=False)
bot.send_markdown(title="北海生活指数", text=indices_message, is_at_all=False)

