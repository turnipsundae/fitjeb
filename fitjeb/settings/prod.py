"""
Production settings.
"""

from fitjeb.settings.base import *

import logging

logger = logging.getLogger(__name__)

# Turn off debug during production
DEBUG = False

# Be more selective about hosts
ALLOWED_HOSTS = ['.elasticbeanstalk.com']

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# Checks for database in environment. If present, use it.
# In this case, database should be RDS PostgreSQL from Amazon.

if 'RDS_HOSTNAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    with open('logfile', 'w') as f:
        f.write('RDS not in environment variables')

STATIC_ROOT = 'static'

# Celery settings with Amazon SQS
# http://docs.celeryproject.org/en/latest/getting-started/brokers/sqs.html
# Broker url format should be 
# sqs://aws_access_key_id:aws_secret_access_key@
# make sure to add @ at end
import urllib

if 'AWS_ACCESS_KEY_ID' in os.environ and 'AWS_SECRET_ACCESS_KEY' in os.environ:
    BROKER_URL = 'sqs://{0}:{1}@'.format(
        urllib.parse.quote(os.environ['AWS_ACCESS_KEY_ID'], safe=''),
        urllib.parse.quote(os.environ['AWS_SECRET_ACCESS_KEY'], safe='')
    )
    BROKER_TRANSPORT_OPTIONS = {'region': 'us-west-2'}

    with open('logfile', 'w') as f:
        f.write('Success')
else:
    with open('logfile', 'w') as f:
        f.write('AWS access keys not in environment variables')
