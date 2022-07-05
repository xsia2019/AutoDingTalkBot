# -*- coding: utf-8 -*-


import datetime

from Lib.bhzhaopin import BeiHaiJob


# 读取文件
def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    try:
        # 定义筛选条件
        salary = 10000
        exc_job = read_file('exclusive_job.txt')
        exc_company = read_file('exclusive_company.txt')

        # 获取招聘信息
        beihaijob = BeiHaiJob(salary=salary, exc_job=exc_job, exc_company=exc_company)
        jobInfo = beihaijob.get_info_format()

        # 汇总消息
        job_message = ''
        for job in jobInfo:
            job_message += job

        # 程序运行信息
        total_count = beihaijob.total_count
        job_count = beihaijob.job_count
        usage = (beihaijob.end_time - beihaijob.start_time).seconds
        message = '总共抓取了{}条招聘信息，其中有{}条有效信息，耗时{}秒'.format(total_count, job_count, usage)

        today = datetime.datetime.today().strftime('%Y-%m-%d')
        print('-' * 20)
        print('即将为你发送 {} 的北海招聘信息  \n  '.format(today))
        print("北海招聘信息")
        print(job_message)
        print("程序运行信息")
        print(message)
        print("Copyright")
        print('Power by AutoDingTalkBot on Github Actions  \n  ')
        print('-' * 20)

    except Exception as e:
        print(e)
        print('发送失败')
