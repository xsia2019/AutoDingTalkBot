from Lib.gxrcapi import GXRCAPI

if __name__ == '__main__':
    gxjob = GXRCAPI()

    job_messange = gxjob.get_filter_message()
    for job in job_messange:
        print(job)
