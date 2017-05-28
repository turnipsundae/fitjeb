from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitjeb.settings.base')

import urllib

if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:

    app = Celery('fitjeb', broker='sqs://{0}:{1}@'.format(
        urllib.parse.quote(os.environ['AWS_ACCESS_KEY_ID'], safe=''),
        urllib.parse.quote(os.environ['AWS_SECRET_ACCESS_KEY'], safe='')
    ))
    with open('logfile', 'w') as f:
        f.write('Success')
else:
    app = Celery('fitjeb')
    with open('logfile', 'w') as f:
        f.write('AWS access keys not in environment variables')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
