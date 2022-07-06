# 查询北海365招聘网上的职位信息
# https://www.365zhaopin.com/
# -*- coding: utf-8 -*-

import datetime
import random
import re
import time

import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent


# 根据关键字列表生成re过滤器
def get_pattern(words):
    if words is not None:
        keywords = [word.strip() for word in words.split(',') if word]
        pattern = '|'.join(keywords)
        return re.compile(pattern)
    else:
        return None


# 处理工资
def get_salary_right(salary):
    try:
        if re.search(r'（底薪([\d]{1,6}[-]?){1,2}', salary):
            salary = re.search(r'（底薪([\d]{1,6}[-]?){1,2}', salary).group()[3:]
        elif re.search(r'面议', salary):
            salary = 0
        elif re.search(r'￥([\d]{1,6}[-]?){1,2}', salary):
            salary = re.search(r'￥([\d]{1,6}[-]?){1,2}', salary).group()[1:]
        else:
            salary = salary

        if salary == 0:
            salary = '0'
        elif '-' in salary:
            salary = salary.split('-')
            salary = salary[0]
        else:
            salary = re.search(r'\d{2,6}', salary).group().strip()

        return salary
    except:
        return 0


class BeiHaiJob(object):
    def __init__(self, salary=10000, exc_job=None, exc_company=None, ):
        self.headers = {'User-Agent': user_agent()}  # 取得ua
        # 北海365招聘网职位信息列表首页
        self.url = 'https://www.365zhaopin.com/index.php?do=search&sorttype=1&salary_id=5&p='
        # 北海365招聘网主页
        self.homepage = 'https://www.365zhaopin.com/'
        # 接收关键字
        self.salary = salary       # 薪水标准默认10000
        self.exc_job = exc_job
        self.exc_company = exc_company
        # 计数参量
        self.total_count = 0
        self.job_count = 0
        # 运行时间
        self.start_time = datetime.datetime.now()
        self.end_time = None

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

    # 生成链接
    def get_url(self):
        html = self.get_html(self.url + str(1))
        # 获取页数
        total_page = re.search(r'(class="ml20">1/)(\d{1,3})(页)', html).group(2)
        # pattern = re.compile(r'(class="ml20">1/)(\d{1,3})(页)')
        # total_page = re.search(pattern, html).group(2)
        total_page = int(total_page)
        for i in range(1, total_page + 1):
            url = self.url + str(i)
            yield url

    #  解析网页内容
    def get_job_info(self, response):
        job_infos = []
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
                salary = get_salary_right(salary)
                # 公司名称
                company = job_item.find('div', class_='panl10 mt3').get_text().strip()
                # 发布日期
                date = job_item.find('div', class_='panl5').get_text().strip()
                # 详情链接
                url = self.homepage + job_item.find('div', class_='panl1').find('a')['href']

                job_info = [title, salary, company, date, url]
                job_infos.append(job_info)
            return job_infos

        except Exception as e:
            print('error')
            print(e)
            print('error')
            return '解析错误'

    # 筛选职位信息
    def get_filter_job(self):
        flag = True
        # 根据关键字生成pattern
        pattern_job = get_pattern(self.exc_job)
        pattern_company = get_pattern(self.exc_company)
        urls = self.get_url()
        for url in urls:
            html = self.get_html(url)
            job_info = self.get_job_info(html)
            # 筛选职位信息
            for item in job_info:
                title = item[0]
                salary = item[1]
                company = item[2]
                date = item[3]
                # 非今天日期的直接跳出内循环
                if date != '今天':
                    self.end_time = datetime.datetime.now()
                    flag = False
                    break
                elif int(salary) < self.salary:
                    self.end_time = datetime.datetime.now()
                    continue
                elif self.exc_job != '':
                    if re.search(pattern_job, title):
                        continue
                    elif self.exc_company != '':
                        if re.search(pattern_company, company):
                            continue
                        else:
                            yield item
                    else:
                        yield item
                else:
                    yield item
            # 非今天日期的直接跳出外循环
            if not flag:
                break

    # 获取职位信息并格式化输出
    def get_info_format(self):
        # 根据工作
        for job in self.get_filter_job():
            job_title = job[0] + ', '
            job_salary = job[1] + ', '
            job_company = job[2] + ', '
            job_date = job[3] + ', '
            job_url = '[详情](' + job[4] + ')'

            # 返回生成的文字
            yield job_title + job_salary + job_company + job_date + job_url + '  \n  '
