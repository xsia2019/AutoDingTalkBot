# 查询广西人才网上的职位信息
# gxrc.com
# author: kinofgl
# -*- coding: utf-8 -*-

import random
import re
import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent


class GXRC(object):
    def __init__(self, page_num, salary_min, ):
        self.homepage = 'https://www.gxrc.com/'
        # 工作类别：高级管理/人力资源/行政
        self.url = 'https://s.gxrc.com/sCareer?postype=5470&page='
        # 取得User-Agent
        self.headers = {'User-Agent': user_agent()}
        # 最大页数
        self.page_num = page_num
        # 最低工资
        self.salary_min = salary_min
        # 职位信息数据
        self.job_data = []
        # 职位信息列表
        self.job_list = []

    #  获取网页内容
    def get_html(self, url):
        num = 0
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                return response.text
            except:
                num += 1
                print('第 %s 次获取网页内容失败，重新获取...' % num)
                # 尝试3次不成功则放弃
                if num < 3:
                    time.sleep(random.randint(1, 10))  # 随机休眠1-10秒
                    continue
                else:
                    break

    # 2 解析网页内容
    def get_job_info(self, response):
        try:
            soup = BeautifulSoup(response, 'lxml')
            # job_list = soup.find_all('div', class_='rlOne')
            job_items = soup.find_all('ul', class_='posDetailUL clearfix')
            for job_item in job_items:
                job_name = job_item.find('li', class_='w1').find('a').get_text().strip()
                job_company = job_item.find('li', class_='w2').find('a').get_text().strip()
                job_salary = job_item.find('li', class_='w3').get_text().strip()
                job_location = job_item.find('li', class_='w4').get_text().strip()
                job_time = job_item.find('li', class_='w5').get_text().strip()
                job_url = 'https:' + job_item.find('li', class_='w1').find('a').get('href')

                # 处理工资
                if re.search(r'\d+', job_salary):
                    job_salary = re.search(r'([\d]{4,6}[-]?){1,2}', job_salary).group()
                else:
                    job_salary = 0

                if job_salary == 0:
                    job_salary = 0
                elif '-' in job_salary:
                    job_salary = job_salary.split('-')
                    job_salary = job_salary[0]

                list = [job_name, job_company, job_salary, job_location, job_time, job_url]
                self.job_data.append(list)

        finally:
            return self.job_data

    # 获得工作信息
    def get_job_now(self):
        today = datetime.today().date()
        for i in range(1, self.page_num + 1):
            url = self.url + str(i)
            print('正在爬取  \n  %s ' % url)
            time.sleep(random.randint(5, 10))  # 随机休眠5-10秒
            response = self.get_html(url)
            job_info = self.get_job_info(response)
            # 非今天日期就中止
            job_date = datetime.strptime(job_info[0][4], "%Y-%m-%d").date()
            if job_date != today:
                break
            # 根据条件筛选
            for job in job_info:
                print(job)
                if int(job[2]) >= 10000 and \
                        re.search(r'(助理)|(副总)|(行政)|(主管)', job[0]):
                    self.job_list.append(job)

        return self.job_list

    def get_job_message(self, job_data):
        # 处理职位信息
        job_message = ''
        # 发送消息
        for job in job_data:
            job_title = job[0][:4] + ', '
            job_salary = job[2][:5] + ', '
            job_company = job[1][:4] + ', '
            job_location = job[3][:3] + ', '
            job_date = job[4][5:] + ', '
            job_url = '[详情](' + job[5] + ')'

            job_message += job_title + job_salary + job_company + job_date + job_url + '  \n  '

        return job_message


if __name__ == '__main__':
    gxrc = GXRC(100, 10000)
    job_list = gxrc.get_job_now()
    job_message = gxrc.get_job_message(job_list)
    # job_list = gxrc.get_job_now(49)
    print(job_message)
