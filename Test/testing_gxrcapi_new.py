# -*- coding: utf-8 -*-

import datetime
import sys

from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, FeedLink, CardItem

from KEY.dingtalkbot_key import PiPiDou_webhook, PiPiDou_secret
from Lib.gxrcapi_new import GXRCAPI


# 读取文件
def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    try:
        # 接收系统传入的webhook和secret
        # webhook = sys.argv[1]
        # secret = sys.argv[2]
        webhook = PiPiDou_webhook
        secret = PiPiDou_secret

        # 初始化钉钉机器人
        bot = DingtalkChatbot(webhook, secret=secret)

        # 定义筛选条件
        salary = 15000
        job_filter = read_file('../exclusive_job.txt')
        company_filter = read_file('../exclusive_company.txt')

        # 获取招聘信息
        gxrc = GXRCAPI(salary=salary, job_filter=job_filter, company_filter=company_filter)
        # 取得正常工作
        job_message = ''
        job_infos = gxrc.get_today_job()
        for job_info in job_infos:
            job_message += job_info

        # 取得兼职工作信息
        part_time_job_message = ''
        part_time_jobs = gxrc.get_keyword_job('兼职', '英语,翻译')
        for part_time_job in part_time_jobs:
            part_time_job_message += part_time_job + '\n'

            # print(part_time_job)

        today = datetime.datetime.today().strftime('%Y-%m-%d')

        bot.send_markdown(title="Podcast", text='即将为你发送 {} 的广西人才网招聘信息  \n  '.format(today), is_at_all=False)
        bot.send_markdown(title="广西人才网招聘信息", text=job_message, is_at_all=False)
        bot.send_markdown(title="广西人才网兼职信息", text=part_time_job_message, is_at_all=False)
        bot.send_markdown(title="Copyright", text='Power by AutoDingTalkBot on Github Actions  \n  ', is_at_all=False)

    except Exception as e:
        print(e)
        print('发送失败')
