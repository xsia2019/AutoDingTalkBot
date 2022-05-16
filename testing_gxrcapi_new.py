# -*- coding: utf-8 -*-

from gxrcapi_new import GXRCAPI


# 读取文件
def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        return f.read()


if __name__ == '__main__':
    salary = 15000
    job_filter = read_file('exclusive_job.txt')
    company_filter = read_file('exclusive_company.txt')

    gxrc = GXRCAPI(salary=salary, job_filter=job_filter, company_filter=company_filter)
    # 取得正常工作
    job_infos = gxrc.get_today_job()
    for job_info in job_infos:
        print(job_info)
    # 取得兼职工作
    part_time_jobs = gxrc.get_keyword_job('兼职', '英语,翻译')
    for part_time_job in part_time_jobs:
        print(part_time_job)
