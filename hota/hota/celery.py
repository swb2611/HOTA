# your_project/celery.py
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hota.settings")


app = Celery('hota')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'fetch_machine_data': {
        'task': 'api.tasks.monitor_l1',
        'schedule': 10.0,  # 每10秒执行一次
    }
}

