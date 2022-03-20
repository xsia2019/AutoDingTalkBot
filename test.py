# -*- coding: utf-8 -*-

from Lib import gxrcAPI
import csv
from datetime import datetime, timedelta


def get_timestr():
    bjtime = datetime.utcnow() + timedelta(hours=8)
    timestr = bjtime.strftime('%Y%m%d%H%M%S')
    today = bjtime.strftime('%Y-%m-%d')
    return timestr, today


def save_csv(filename, list):
    with open(filename, 'a+', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(list)


finename = 'gxrc_job_data' + get_timestr()[0] + '.csv'

if __name__ == "__main__":
    # my_job_info = []
    #
    gxrc = gxrcAPI.GXRCAPI()
    # job_info = gxrc.get_job_info()
    # today = get_timestr()[1]
    #
    # for info in job_info:
    #     if info[-1] == today:
    #         if int(info[3]) > 10000:        # 薪水大于10000
    #             if re.search(r'(助理)|(副总)|(行政)|(主管)|(总监)', info[1]):     # 匹配职位名称
    #                 my_job_info.append(info)
    #                 print(info)
    #     else:
    #         break
    message = gxrc.get_job_message()
    print(message)