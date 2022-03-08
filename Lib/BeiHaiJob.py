# 查询北海365招聘网上的职位信息
# https://www.365zhaopin.com/
# author: kinofgl
# -*- coding: utf-8 -*-

import random
import re
import time
import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent


class BeiHaiJob(object):
    def __init__(self):
        self.headers = {'User-Agent': user_agent()}  # 取得ua
        self.url = 'https://www.365zhaopin.com/index.php?do=search&p='

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

    #  获取页数
    def get_page_num(self):
        html = self.get_html(self.url + str(1))
        soup = BeautifulSoup(html, 'lxml')
        # 获取页数
        page_num = soup.select('span.ml20')[0].get_text()
        # 处理页数
        page_num = int(page_num[2:5])
        return page_num

    #  解析网页内容
    def get_job_info(self, response):
        job_info = []
        try:
            soup = BeautifulSoup(response, 'lxml')
            # 取得当前页面所有的职位信息
            job_items = soup.select('div.w1024.f-yehei > div.main-ul > ul > li')
            # 遍历职位信息
            for job_item in job_items:
                # 职位名称
                title = job_item.find('div', class_='panl1').find('a').get_text().strip()
                # 职位薪水
                salary = job_item.find('div', class_='panl3 salary-panl3').get_text().strip()
                # 公司名称
                company = job_item.find('div', class_='panl10 mt3').get_text().strip()
                # 发布日期
                date = job_item.find('div', class_='panl5').get_text().strip()

                # 处理工资
                if re.search(r'（底薪([\d]{4,6}[-]?){1,2}', salary):
                    salary = re.search(r'（底薪([\d]{4,6}[-]?){1,2}', salary).group()[3:]
                elif re.search(r'面议', salary):
                    salary = 0
                elif re.search(r'￥([\d]{2,6}[-]?){1,2}', salary):
                    salary = re.search(r'￥([\d]{2,6}[-]?){1,2}', salary).group()[1:]
                else:
                    salary = salary

                if salary == 0:
                    salary = '0'
                elif '-' in salary:
                    salary = salary.split('-')
                    salary = salary[0]
                else:
                    salary = re.search(r'\d{2,6}', salary).group().strip()

                list = [title, salary, company, date]
                job_info.append(list)
            return job_info

        except Exception as e:
            print(e)
            return '解析错误'

    #  获取职位信息
    def get_job_now(self):
        job_list = []
        for i in range(1, self.get_page_num() + 1):
            # 开始抓取
            html = self.get_html(self.url + str(i))
            job_info = self.get_job_info(html)
            # 如果不是今天的信息，中止抓取
            if job_info[0][3] != '今天':
                break

            for item in job_info:
                if int(item[1]) > 7999 and \
                        re.search(r'(助理)|(副总)|(行政)|(主管)', item[0]) and \
                        item[3] == '今天':
                    job_list.append(item)
                    pass
                else:
                    continue

        return job_list
