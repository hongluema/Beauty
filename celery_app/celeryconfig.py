# encoding: utf-8
from datetime import datetime, timedelta
from celery.schedules import crontab


# BROKER_URL = 'redis://:crs-0ng0ncpo:kUk8Rd023t4o@10.66.131.159:6379' # 指定Broker, 招财火配置
# CELERY_RESULT_BACKEND = 'redis://:crs-0ng0ncpo:kUk8Rd023t4o@10.66.131.159:6379/0' # 指定Backend, 招财火配置
BROKER_URL = 'redis://127.0.0.1:6379' # 指定Broker
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0' # 指定Backend
CELERY_TIMEZONE = 'Asia/Shanghai' # 指定时区， 默认是 UTC
CELERY_IMPORTS = ( # 指定导入的任务模块
        'celery_app.task1',
        'celery_app.send_email',
        )

# schedules
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'celery_app.task1.add',
         'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
         'args': (5, 8)                           # 任务函数参数
    },
    'multiply-at-some-time': {
        'task': 'celery_app.task1.multiply',
        'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
        'args': (3, 7)                            # 任务函数参数
    }
}