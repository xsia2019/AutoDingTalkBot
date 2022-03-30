# -*- coding: utf-8 -*-
import re
import sys
import time

from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem
from Lib.BeiHaiJob import BeiHaiJob
from Lib.gxrcAPI import GXRCAPI
from KEY.dingtalkbot_key import PiPiDou_webhook, PiPiDou_secret
import csv

filename = 'JobTitle.csv'


def get_job_title(file):
    with open(file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            yield row[0]


def save_job_title(file, job_title):
    with open(file, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([job_title])


if __name__ == '__main__':
    try:

        # 接收系统传入的webhook和secret
        # webhook = sys.argv[1]
        # secret = sys.argv[2]

        # 本地测试用
        webhook = PiPiDou_webhook
        secret = PiPiDou_secret
        # 初始化
        bot = DingtalkChatbot(webhook, secret=secret)

        # 获取招聘信息
        # beiHaiJob = BeiHaiJob()
        # jobInfo = beiHaiJob.get_job_now(10000)
        # bhjob_message = jobInfo[1]
        # bhjob_url = jobInfo[2]
        # 获取gxrc招聘信息
        gxrc = GXRCAPI()
        job_info = gxrc.get_job_info()
        for job in job_info:
            print(job[1])
            save_job_title(filename, job[1])
        # message = gxrc.get_my_job_message()
        #
        # # 发送消息
        # # bot.send_markdown(title="北海招聘信息", text=bhjob_message, is_at_all=False)
        # for m in message:
        #     bot.send_markdown(title="广西人才网", text=m, is_at_all=False)
        #     time.sleep(5)
        # bot.send_markdown(title="Copyright", text='By beihaijob.py, AutoDingTalkBot  \n  ', is_at_all=False)

    except Exception as e:
        print(e)
        print('发送失败')
