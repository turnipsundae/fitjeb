from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitjeb.settings.base')

# app = Celery('fitjeb', broker="sqs://AKIAILCB5LDQT5PORQWQ:+eny2pQ5sqGZqOSPwHLEDevmaza6sd47K2zbCc7D@")
app = Celery('fitjeb')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
# app.config_from_object('fitjeb.settings.base', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
