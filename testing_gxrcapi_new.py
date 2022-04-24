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
    job_infos = gxrc.get_today_job()
    for job in job_infos:
        print(job)

    # 程序运行信息
    total_count = gxrc.total_count
    job_count = gxrc.job_count
    usage = (gxrc.end_time - gxrc.start_time).seconds
    message = '总共抓取了{}条招聘信息，其中有{}条有效信息，耗时{}秒'.format(total_count, job_count, usage)
    print('-' * 50)
    print(message)
    print('-' * 50)
