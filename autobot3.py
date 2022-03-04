# -*- coding: utf-8 -*-


from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem
from Eduic.DailySentence import EduicContent
from KEY.dingtalkbot_key import PiPiDou_webhook, PiPiDou_secret


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
