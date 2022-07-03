# 查询www.gxrc.com的工作信息
# 参考：https://www.gxrc.com/
# -*- coding: utf-8 -*-

import datetime
import random
import re
import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from fake_user_agent.main import user_agent


# 根据关键字列表生成re过滤器
def get_pattern(words):
    if words is not None:
        keywords = [word.strip() for word in words.split(',') if word]
        pattern = '|'.join(keywords)
        return re.compile(pattern)
    else:
        return None


# 生成日期和时间
def get_time_str():
    bj_time = datetime.utcnow() + timedelta(hours=8)
    time_str = bj_time.strftime('%Y%m%d%H%M%S')
    today = bj_time.strftime('%Y-%m-%d')
    return time_str, today


# 获取筛选的职位信息
def today_pattern():
    today = get_time_str()[1]
    return re.compile(today)


class GXRCAPI(object):

    def __init__(self, salary=10000, job_filter=None, company_filter=None,):

        self.salary = salary
        self.job_filter = get_pattern(job_filter)
        self.company_filter = get_pattern(company_filter)

        self.url = 'https://s.gxrc.com/sJob?orderType={channel}&page=1'
        self.headers = {'User-Agent': user_agent()}
        self.session = requests.Session()

        self.channel_url = 'https://s.gxrc.com/sCareer?posType={channel}'
        self.category = [
            5467, 5468, 5469, 5470, 5471, 5472,
            5473, 5474, 5475, 5476, 5477, 5478,
        ]
        self.keyword_url = 'https://s.gxrc.com/sJob?keyword='

        # 计数参数
        self.total_count = 0
        self.job_count = 0
        # 运行时间
        self.start_time = datetime.now()
        self.end_time = None


    # 获取每个频道的总页数，后生成频道总链接
    def get_channel_urls(self, channel):
        # 根据频道首页获取总页数
        channel_url = self.channel_url.replace('{channel}', str(channel))
        html = self.get_html(channel_url)
        if html:
            result = re.search(r'(pgInfo_last.*?>)(\d{3})(\+?<\/i>)', html).group(2)
            total_page = int(result)
            # 生成频道所有链接
            for page_num in range(total_page):
                url = self.url.replace('{channel}', str(channel))
                yield url[:-1] + str(page_num + 1)
        else:
            return None

    # 获取每个频道链接包含的职位信息
    def extract_job(self, response):
        try:
            soup = BeautifulSoup(response, 'lxml')
            job_items = soup.select('#posList div.rlOne')
            # 遍历职位信息
            for job_info in job_items:
                # 获取职位名称
                job_name = job_info.find('li', class_='w1').find('a').get_text().strip()
                # 获取公司名称
                job_company = job_info.find('li', class_='w2').find('a').get_text().strip()
                # 获取薪资
                job_salary = job_info.find('li', class_='w3').get_text().strip()
                # 修正薪水信息
                if re.search(r'(\d{3,6}-?)+', job_salary):
                    job_salary_low = job_salary.split('-')[0]
                    job_salary_high = job_salary.split('-')[1]
                else:
                    job_salary_low = '0'
                    job_salary_high = '0'
                # 获取公司地址
                job_address = job_info.find('li', class_='w4').get_text().strip()
                # 获取发布时间
                job_time = job_info.find('li', class_='w5').get_text().strip()
                # 获取职位简介
                job_posInfo = job_info.find('span', class_='posInfo').get_text().strip()
                # 获取职位链接
                job_url = 'https:' + job_info.find('li', class_='w1').find('a')['href'].strip()

                yield job_name, job_company, job_salary_low, job_salary_high, \
                      job_address, job_time, job_posInfo, job_url
        except Exception as e:
            print('extract_job')
            print(e)

    # 得到筛选过的职位信息
    def get_today_job(self):
        # 取得频道ID
        for channel in self.category:
            print('channel:', channel)
            for url in self.get_channel_urls(channel):
                # 开始获取每个频道页面的职位信息
                html = self.get_html(url)
                # 解析html得到职位信息
                job_info = self.extract_job(html)
                for job in job_info:
                    name = job[0]
                    company = job[1]
                    salary = int(job[2])
                    date = job[5]
                    # 筛选日期
                    if today_pattern().search(date):
                        # 筛选薪水筛选岗位筛选公司
                        if salary < self.salary or \
                                self.job_filter.search(name) or \
                                self.company_filter.search(company):
                            continue
                        else:
                            job_message = self.get_info_format(job)
                            yield job_message
                    else:
                        break

    # 获取页面html
    def get_html(self, url):
        num = 0
        while True:
            try:
                response = self.session.get(url, headers=self.headers, timeout=30)
                response.encoding = 'utf-8'
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

    # 获取关键字的信息
    def get_keyword_job(self, keyword, content):
        keyword = keyword.strip()
        content = content.strip()
        for i in range(1, 10):
            # 得到链接
            url = self.keyword_url + keyword + '&page=' + str(i)
            # 得到关键字的页面html
            html = self.get_html(url)
            # 获取页面的职位信息
            job_info = self.extract_job(html)
            for job in job_info:
                # 总职位数计数+1
                self.total_count += 1
                name = job[0]
                date = job[5]
                job_posInfo = job[6]
                # 筛选日期
                if today_pattern().search(date):
                    # 筛选职位
                    content_filter = get_pattern(content)
                    if content_filter.search(name) or content_filter.search(job_posInfo):
                        message = self.get_info_format(job)
                        yield message
                    else:
                        continue
                else:
                    break

    def get_info_format(self, job):
        job_title = job[0] + ', '
        job_salary = job[2] + ', '
        job_company = job[1] + ', '
        job_date = job[5] + ', '
        job_posInfo = job[6] + ', '
        job_url = '[详情](' + job[7] + ')'
        # 返回生成的文字
        # return job_title + job_salary + job_company + job_date + job_posInfo + job_url + '  \n  '
        result = job_title + job_salary + job_company + job_date + job_url + '  \n  '
        return result
