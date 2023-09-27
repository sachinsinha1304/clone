# from apscheduler.schedulers.background import BackgroundScheduler
# from datetime import datetime
#
# t = 5
# def job():
#     global t
#     if t == 0:
#         print('test over')
#     else:
#         print(f'Current time is {t}')
#         t -= 1
#
#
# def start():
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(job, 'interval',minutes = 1,id = 'rem001', replace_existing=True)
#     scheduler.start()