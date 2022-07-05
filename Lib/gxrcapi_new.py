# 查询www.gxrc.com的工作信息
# 参考：https://www.gxrc.com/
# -*- coding: utf-8 -*-

import datetime
import random
import re
import time
from datetime import datetime, timedelta

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


# 解析正确的薪水
def get_right_salary(salary):
    if not re.search(r'-', salary) and re.search(r'[\u4e00-\u9fa5]', salary):
        job_salary_low = re.search(r'\d*', salary).group()
        job_salary_high = re.search(r'\d*', salary).group()
    elif re.search(r'(\d{3,6}-?)+', salary):
        job_salary_low = salary.split('-')[0]
        job_salary_high = salary.split('-')[1]
    elif salary == '':
        job_salary_low = 0
        job_salary_high = 0
    else:
        job_salary_low = 0
        job_salary_high = 0
    return int(job_salary_low), int(job_salary_high)


class GXRCAPI(object):
    def __init__(self, salary=10000, job_filter=None, company_filter=None, ):

        self.salary = salary
        self.job_filter = job_filter
        self.company_filter = company_filter

        self.url = 'https://s.gxrc.com/sJob?schType=1&pageSize=20&orderType=1&page={page_num}'
        self.url = 'https://s.gxrc.com/sJob?schType=1&salary={salary_lev}&page={page_num}'
        self.salary_list = [811, 812, 813, 1039, 1040]

        self.headers = {'User-Agent': user_agent()}
        self.session = requests.Session()

        # 计数参数
        self.total_count = 0
        self.job_count = 0
        # 运行时间
        self.start_time = datetime.now()
        self.end_time = None

    def get_urls_test(self):
        for salary_lev in self.salary_list:
            url = self.url.replace('{salary_lev}', str(salary_lev))
            yield url

    # 获取每个频道的总页数，后生成频道总链接
    def get_urls(self):

        # 生成频道所有链接
        for page_num in range(500):
            url = self.url.replace('{page_num}', str(page_num + 1))
            yield url
        else:
            return None

    # 获取每个频道链接包含的职位信息
    def get_job_info(self, response):
        job_infos = []
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
                job_salary_low = get_right_salary(job_salary)[0]
                job_salary_high = get_right_salary(job_salary)[1]
                # 获取公司地址
                job_address = job_info.find('li', class_='w4').get_text().strip()
                # 获取发布时间
                job_time = job_info.find('li', class_='w5').get_text().strip()
                # 获取职位简介
                job_posInfo = job_info.find('span', class_='posInfo').get_text().strip()
                # 获取职位链接
                job_url = 'https:' + job_info.find('li', class_='w1').find('a')['href'].strip()

                extract_job_info = [job_name, job_company, job_salary_low, job_salary_high,
                                    job_address, job_time, job_posInfo, job_url]
                job_infos.append(extract_job_info)

            return job_infos

        except Exception as e:
            print('extract_job')
            print(e)

    # 得到筛选过的职位信息
    def get_filter_job(self):
        flag = True
        today = today_pattern()
        # 根据关键字生成pattern
        pattern_job = get_pattern(self.job_filter)
        pattern_company = get_pattern(self.company_filter)
        urls = self.get_urls()
        for url in urls:
            html = self.get_html(url)
            job_info = self.get_job_info(html)
            for job in job_info:
                # 总职位加1
                self.total_count += 1
                title = job[0]
                company = job[1]
                salary = int(job[2])
                date = job[5]
                # 筛选今天的日期
                if not today.search(date):
                    flag = False
                    break
                    # 筛选薪水筛选岗位筛选公司
                elif salary < self.salary:
                    continue
                elif self.job_filter != '':
                    if pattern_job.search(title):
                        continue
                    elif self.company_filter != '':
                        if pattern_company.search(company):
                            continue
                        else:
                            self.job_count += 1
                            yield job
                    else:
                        self.job_count += 1
                        yield job
                else:
                    self.job_count += 1
                    yield job
            if not flag:
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
                    time.sleep(random.randint(10, 20))  # 随机休眠1-10秒
                    continue
                else:
                    break

    def get_info_format(self):
        for job in self.get_filter_job():
            job_title = job[0] + ', '
            job_salary = str(job[2]) + ', '
            job_company = job[1] + ', '
            job_date = job[5] + ', '
            job_posInfo = job[6] + ', '
            job_url = '[详情](' + job[7] + ')'
            # 返回生成的文字
            # return job_title + job_salary + job_company + job_date + job_posInfo + job_url + '  \n  '
            result = job_title + job_salary + job_company + job_date + job_url + '  \n  '
            yield result


def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    salary = 10000
    exc_job = read_file('../exclusive_job.txt')
    exc_company = read_file('../exclusive_company.txt')

    # 获取招聘信息
    gxjob = GXRCAPI(salary=salary, job_filter=exc_job, company_filter=exc_company, )

    job_infos = gxjob.get_info_format()
    for job in job_infos:
        print(job)
    # url = 'https://s.gxrc.com/sJob?schType=1&pageSize=20&orderType=1&page=22'
    # html = gxjob.get_html(url)
    # job_info = gxjob.get_job_info(html)
    # for info in job_info:
    #     print(info)

    total_job = gxjob.job_count
    total_count = gxjob.total_count

    print(total_job, total_count)
