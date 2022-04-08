# 查询www.gxrc.com的工作信息
# -*- coding: utf-8 -*-
import random
import re
import time
import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent
from datetime import datetime, timedelta


def get_timestr():
    bjtime = datetime.utcnow() + timedelta(hours=8)
    timestr = bjtime.strftime('%Y%m%d%H%M%S')
    today = bjtime.strftime('%Y-%m-%d')
    return timestr, today


def get_keyword_pattern(word_list):
    new_keyword = ''
    for w in word_list.split(','):
        new_keyword += w.strip() + '|'
    return re.compile(new_keyword[:-1])


class GXRCAPI(object):
    def __init__(self):
        self.headers = {'User-Agent': user_agent()}
        # 所有职位列表url
        url = 'https://s.gxrc.com/sJob?orderType=1&page=1'
        raw_url = 'https://s.gxrc.com/sCareer?page=2&posType=5467'
        self.channel_url = 'https://s.gxrc.com/sCareer?'
        # self.category = [
        #     5467, 5468, 5469, 5470, 5471, 5472,
        #     5473, 5474, 5475, 5476, 5477, 5478,
        # ]
        self.category = [
            5470,
        ]

    # 获取每个职位频道的的所有url
    def get_url(self):
        # 得到初始url
        for i in self.category:
            url = 'https://s.gxrc.com/sCareer?posType={id}&page=1'.format(id=i)
            html = self.get_html(url)
            soup = BeautifulSoup(html, 'lxml')
            page = soup.find('div', class_='page').find('i', id='pgInfo_last').get_text().strip()[0:3]
            page = int(page)
            for num in range(1, page + 1):
                url = self.channel_url + 'posType={id}&page={page}'.format(id=i, page=num)
                yield url

    # 获取每个职位频页面的工作内容
    def get_job_item(self):
        try:
            for url in self.get_url():
                html = self.get_html(url)
                soup = BeautifulSoup(html, 'lxml')
                job_item = soup.select('#posList')
                # for item in job_item:
                #     yield item
                yield job_item
        except Exception as e:
            print(e)

    # 根据job_item来获得各个信息
    def get_job_info_all(self):
        try:
            for info in self.get_job_item():
                for job_info in info:
                    # 获取职位链接
                    job_url = job_info.find('li', class_='w1').find('a')['href'].strip()
                    job_url =  'https:' + job_url
                    # 获取职位名称
                    job_name = job_info.find('li', class_='w1').find('a').get_text().strip()
                    # 获取公司名称
                    job_company = job_info.find('li', class_='w2').find('a').get_text().strip()
                    # 获取薪资
                    job_salary = job_info.find('li', class_='w3').get_text().strip()
                    # 修正薪水信息
                    if ('-' in job_salary) and re.search(r'(\d{3,6}-?)+', job_salary):
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

                    yield job_url, job_name, job_company, job_salary_low, job_salary_high, \
                          job_address, job_time, job_posInfo

        except Exception as e:
            print(e)

    # 根据条件筛选
    def get_my_job_info(self, date='Today', salary=10000, inclusive=None, exclusive=None):
        # 取得今天日期
        today = get_timestr()[1] if date == 'Today' else date
        salary = salary
        inclusive = get_keyword_pattern(inclusive)
        exclusive = get_keyword_pattern(exclusive)

        for info in self.get_job_info_all():
            if info[-2] == today:  # 过滤非今天日期信息
                # if re.search(r'(营销)|(经营)', info[1]): # 过滤特定职位名称
                if exclusive.search(info[1]): # 过滤特定职位名称
                    continue
                if int(info[3]) > salary:  # 薪水大于10000
                    # if re.search(r'(助理)|(副总)|(行政)|(主管)|(总监)', info[1]):  # 匹配职位名称
                    if inclusive.search(info[1]):  # 匹配职位名称
                        # my_job_info.append(info)
                        # print(info)
                        yield info
            else:
                break

    # 从列表页面获取每个职位的url及其他信息
    def get_job_info(self):
        for url in self.get_url():
            html = self.get_html(url)
            soup = BeautifulSoup(html, 'lxml')
            # 所有内容列表
            job_items = soup.find('div', class_='posDetailWrap').find_all('div', class_='rlOne')
            try:
                for job_info in job_items:
                    job_url = 'https:' + job_info.find('li', class_='w1').find('a')['href'].strip()
                    job_name = job_info.find('li', class_='w1').find('a').get_text().strip()
                    job_company = job_info.find('li', class_='w2').find('a').get_text().strip()
                    job_salary = job_info.find('li', class_='w3').get_text().strip()
                    # 修正薪水信息
                    if ('-' in job_salary) and re.search(r'(\d{3,6}-?)+', job_salary):
                        job_salary_low = job_salary.split('-')[0]
                        job_salary_high = job_salary.split('-')[1]
                    else:
                        job_salary_low = '0'
                        job_salary_high = '0'

                    job_address = job_info.find('li', class_='w4').get_text().strip()
                    job_time = job_info.find('li', class_='w5').get_text().strip()
                    job_posInfo = job_info.find('span', class_='posInfo').get_text().strip()

                    # job_info_dict = {
                    #     'job_url': job_url,
                    #     'job_name': job_name,
                    #     'job_company': job_company,
                    #     'job_salary': job_salary,
                    #     'job_address': job_address,
                    #     'job_time': job_time,
                    # }

                    yield job_url, job_name, job_company, job_salary_low, job_salary_high, job_address, job_time, job_posInfo
            except Exception as e:
                print(url)
                print(e)

    # 过滤职位信息
    # def get_my_job_info(self, date='Today', salary=14999):
    #     my_job_info = []
    #     del_job_title_pattern = re.compile(r'(营销)|(经营)|(招商)|(运营)|(生产)|(财务)')
    #     sel_job_title_pattern = re.compile(r'(助理)|(副总)|(行政)|(主管)|(总监)')
    #     # 取得今天日期
    #     today = get_timestr()[1] if date == 'Today' else date
    #     for info in self.get_job_info():
    #         if info[-2] == today:  # 过滤非今天日期信息
    #             # if re.search(r'(营销)|(经营)', info[1]): # 过滤特定职位名称
    #             if del_job_title_pattern.search(info[1]): # 过滤特定职位名称
    #                 continue
    #             if int(info[3]) > salary:  # 薪水大于10000
    #                 # if re.search(r'(助理)|(副总)|(行政)|(主管)|(总监)', info[1]):  # 匹配职位名称
    #                 if sel_job_title_pattern.search(info[1]):  # 匹配职位名称
    #                     # my_job_info.append(info)
    #                     # print(info)
    #                     yield info
    #         else:
    #             break
    #     # return my_job_info

    # 处理职位信息
    def get_job_message(self):
        job_message = ''
        # 发送消息
        for job in self.get_my_job_info():
            job_title = job[1][:4] + ', '
            job_salary = job[3][:5] + ', '
            job_company = job[2][:6] + ', '
            job_date = job[6][5:] + ', '
            job_url = '[详情](' + job[0] + ')'

            job_message += job_title + job_salary + job_company + job_date + job_url + '  \n'
        yield job_message

    def get_my_job_message(self):
        today = get_timestr()[1]
        for info in self.get_job_info():
            job_message = ''
            if info[-2] == today:  # 过滤非今天日期信息
                if int(info[3]) > 14999:  # 薪水大于10000
                    if re.search(r'(助理)|(副总)|(行政)|(主管)|(总监)', info[1]):  # 匹配职位名称
                        title = info[1] + ', '
                        salary = info[3] + ', '
                        company = info[2] + ', '
                        date = info[6] + ', '
                        url = '[详情](' + info[0] + ')'
                        posInfo = info[7]
                        job_message += title + salary + company + date + url + '  \n' + posInfo + '  \n'
                        yield job_message
            else:
                break

    def get_filter_message(self, job_name=''):

        today = get_timestr()[1]
        for info in self.get_job_info():
            job_message = ''
            if info[-2] == today:  # 过滤非今天日期信息
                if int(info[3]) > 14999:  # 薪水大于10000
                    if re.search(r'(助理)|(副总)|(行政)|(主管)|(总监)', info[1]):  # 匹配职位名称
                        title = info[1] + ', '
                        salary = info[3] + ', '
                        company = info[2] + ', '
                        date = info[6] + ', '
                        url = '[详情](' + info[0] + ')'
                        posInfo = info[7]
                        job_message += title + salary + company + date + url + '  \n' + posInfo + '  \n'
                        yield job_message
            else:
                break

    #  根据url取得网页htm内容
    def get_html(self, url):
        # 尝试3次获取网页
        num = 0
        while True:
            try:
                time.sleep(random.randint(1, 3))
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

    # 生成关键字pattern
    # 当前时间截点
