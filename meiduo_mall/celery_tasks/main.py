from celery import Celery

import os

if not os.getenv('DJANGO_SETTINGS_MODULE'):
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo_mall.settings.dev'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings.pord')

celery_app = Celery('meiduo')

celery_app.config_from_object('celery_tasks.config')

# 自动注册 celery 任务
celery_app.autodiscover_tasks(['celery_tasks.sms', 'celery_tasks.email', 'celery_tasks.html'])
