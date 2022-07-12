# -*- coding: utf-8 -*-

import datetime

from Lib.gxrcapi_new import GXRCAPI


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


def get_group_message(list):
    total = len(list)
    count = 0
    remain = total - count
    start = 0
    step = 30

    while remain > 0:
        info = list[start:start + step]
        job_info = ''
        for item in info:
            job_info += item
        start += step
        count += step
        remain = total - count
        yield job_info


if __name__ == '__main__':
    try:
        # 本地测试开始
        # webhook = PiPiDou_webhook
        # secret = PiPiDou_secret
        # 本地测试结束

        # # 接收系统传入的webhook和secret
        # webhook = sys.argv[1]
        # secret = sys.argv[2]
        #
        # # 初始化钉钉机器人
        # bot = DingtalkChatbot(webhook, secret=secret)

        # 定义筛选条件
        salary = 10000
        exc_job = read_file('./exclusive_job.txt')
        exc_company = read_file('./exclusive_company.txt')

        # 获取招聘信息
        gxjob = GXRCAPI(salary=salary, job_filter=exc_job, company_filter=exc_company, )
        job_infos = gxjob.get_info_format()

        # 汇总消息
        job_message = []
        for job in job_infos:
            job_message.append(job)

        # 程序运行信息
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        print('即将为你发送 {} 的广西人才网招聘信息  \n  '.format(today))

        job_count = gxjob.job_count
        total_count = gxjob.total_count

        for job in get_group_message(job_message):
            print(job)

        message = '总共抓取了{}条招聘信息，其中有{}条有效信息。'.format(total_count, job_count)
        print(message)



    except Exception as e:
        print(e)
        print('发送失败')
