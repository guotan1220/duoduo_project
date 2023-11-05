#############下面两行，耗费了我一天半的时间##############
import os
os.environ.setdefault('DjANGO_SETTINGS_MODULE', 'duoduoshop.settings')
# 注意，celery启动应该在项目文件夹，如最外层的duoduoshop下
# 注意！！！！！！celery_demo下面的文件引用必须要从celery_demo这个celery根目录开始使用绝对路径，不然容易出问题
from celery import Celery
cel = Celery('CeleryDemo',
             broker='redis://127.0.0.1:6379/15', # 这里使用redis作为中间件以及结果存储
             backend='redis://127.0.0.1:6379/14',
             include=[
                 'celery_demo.cms.tasks',
                 'celery_demo.email.tasks'
             ])
# include参数用于导入事件的文件导入地址
# celery_demo.sms_tasks 即celery_demo项目下的sms_tasks
# 时区
cel.conf.timezone = 'Asia/Shanghai'

# 是否使用UTC
cel.conf.enable_utc = False