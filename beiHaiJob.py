# -*- coding: utf-8 -*-

import sys
from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem
from Lib.BeiHaiJob import BeiHaiJob

if __name__ == '__main__':
    try:
        # 接收系统传入的webhook和secret
        webhook = sys.argv[1]
        secret = sys.argv[2]
        # 初始化
        bot = DingtalkChatbot(webhook, secret=secret)

        # 获取招聘信息
        beiHaiJob = BeiHaiJob()
        jobInfo = beiHaiJob.get_job_now()
        job_message = ''
        # 发送消息
        for job in jobInfo:
            for i in range(len(job)):
                job_message += job[i] + ', '
            job_message += '  \n  '

        bot.send_markdown(title="工作信息", text=job_message, is_at_all=False)
