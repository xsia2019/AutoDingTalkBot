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
    def __init__(self, salary=10000, exclusive=None):
        self.headers = {'User-Agent': user_agent()}  # 取得ua
        self.url = 'https://www.365zhaopin.com/index.php?do=search&p='
        self.homepage = 'https://www.365zhaopin.com/'
        self.salary = salary
        self.exclusive = exclusive

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
                # 详情链接
                url = self.homepage + job_item.find('div', class_='panl1').find('a')['href']

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

                job_info = [title, salary, company, date, url]
                yield job_info

        except Exception as e:
            print(e)
            return '解析错误'

    #  获取今天的职位信息
    def get_today_job(self):
        """
        :return: 返回主要职位信息
        """
        # 取得总页数
        page_num = self.get_page_num()
        # 根据页数生成url
        for i in range(1, page_num + 1):
            # 开始抓取html
            html = self.get_html(self.url + str(i))
            # 解析html得到职位信息
            job_info = self.get_job_info(html)
            # 根据薪水标准筛选职位信息
            for item in job_info:
                # 如果不是今天发布的职位信息，中止抓取
                if item[3] != '今天':
                    break
                else:
                    yield item

    # 筛选职位信息
    def filter_job(self):
        for job_info in self.get_today_job():
            title = job_info[0]
            salary = int(job_info[1])
            # 职位薪水大于等于设定值
            if salary >= self.salary:
                # 如果设定了筛选职位信息，则根据关键字筛选（去除）
                if self.exclusive is not None:
                    # 根据关键字生成pattern
                    pattern = self.get_pattern(self.exclusive)
                    # 如果职位名称中包含关键字，则抛弃，否则返回职位信息
                    if re.search(pattern, title):
                        continue
                    else:
                        yield job_info
                # 如果没有设定筛选职位信息，则直接返回
                else:
                    yield job_info
            else:
                continue

    # 根据关键字列表生成re过滤器
    def get_pattern(self, words):
        if words is not None:
            keywords = [word.strip() for word in words.split(',') if word]
            pattern = '|'.join(keywords)
            return re.compile(pattern)
        else:
            return None


    # 获取职位信息并格式化输出
    def get_job_info_format(self):
        job_message = ''
        # 根据工作
        for job in self.filter_job():
            job_title = job[0] + ', '
            job_salary = job[1] + ', '
            job_company = job[2] + ', '
            job_date = job[3] + ', '
            job_url = '[详情](' + job[4] + ')'

            job_message += job_title + job_salary + job_company + job_date + job_url + '  \n  '

        yield job_message
