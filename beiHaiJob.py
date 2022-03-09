# -*- coding: utf-8 -*-

import sys
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem
from Lib.BeiHaiJob import BeiHaiJob
from KEY.dingtalkbot_key import PiPiDou_webhook, PiPiDou_secret

if __name__ == '__main__':
    try:
        # 接收系统传入的webhook和secret
        # webhook = sys.argv[1]
        # secret = sys.argv[2]
        webhook = PiPiDou_webhook
        secret = PiPiDou_secret
        # 初始化
        bot = DingtalkChatbot(webhook, secret=secret)

        # 获取招聘信息
        beiHaiJob = BeiHaiJob()
        jobInfo = beiHaiJob.get_job_now(10000)
        job_message = jobInfo[1]
        # 发送消息
        bot.send_markdown(title="北海招聘信息", text=job_message, is_at_all=False)
    except Exception as e:
        print(e)
        print('发送失败')
