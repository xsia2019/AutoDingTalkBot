# -*- coding: utf-8 -*-

import datetime
import sys

from dingtalkchatbot.chatbot import DingtalkChatbot

from Lib.bhzhaopin import BeiHaiJob


# 本地测试导入

# 读取文件
def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    try:
        # 本地测试开始
        # webhook = PiPiDou_webhook
        # secret = PiPiDou_secret
        # 本地测试结束

        # 接收系统传入的webhook和secret
        webhook = sys.argv[1]
        secret = sys.argv[2]

        # 初始化钉钉机器人
        bot = DingtalkChatbot(webhook, secret=secret)

        # 定义筛选条件
        salary = 8000
        exc_job = read_file('exclusive_job.txt')
        exc_company = read_file('exclusive_company.txt')

        # 获取招聘信息
        beihaijob = BeiHaiJob(salary=salary, exc_job=exc_job, exc_company=exc_company)
        jobInfo = beihaijob.get_info_format()
        # 汇总消息
        job_message = ''
        for job in jobInfo:
            job_message += job
        if len(job_message) == 0:
            job_message = '暂无合适的信息'

        # 程序运行信息
        total_count = beihaijob.total_count
        job_count = beihaijob.job_count
        usage = (beihaijob.end_time - beihaijob.start_time).seconds
        message = '总共抓取了{}条招聘信息，其中有{}条有效信息，耗时{}秒'.format(total_count, job_count, usage)

        today = datetime.datetime.today().strftime('%Y-%m-%d')

        bot.send_markdown(title="Podcast", text='即将为你发送 {} 的北海招聘信息  \n  '.format(today), is_at_all=False)
        bot.send_markdown(title="北海招聘信息", text=job_message, is_at_all=False)
        bot.send_markdown(title="程序运行信息", text=message, is_at_all=False)
        bot.send_markdown(title="Copyright", text='Power by AutoDingTalkBot on Github Actions  \n  ', is_at_all=False)

    except Exception as e:
        print(e)
        print('发送失败')