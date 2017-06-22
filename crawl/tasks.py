# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from crawl.models import Crawled

from datetime import datetime

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="celery_test",
    ignore_result=True
)
def celery_test():
    c = Crawled(link="www.crossfit.com/workout/2017/01/01",
                date=datetime.now(),
                success="True")
    c.save()
    logger.info("Test successful")
