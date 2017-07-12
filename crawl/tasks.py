# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger
from crawl.models import Workout
from crawl.settings import CROSSFIT_WOD_URL, CRAWLER_FREQ_MINUTE, CRAWLER_FREQ_HOUR, CRAWLER_START_DATE
from crawl.utils import save_wod

from datetime import datetime

logger = get_task_logger(__name__)

@periodic_task(
    run_every=(crontab(minute=CRAWLER_FREQ_MINUTE, hour=CRAWLER_FREQ_HOUR)),
    name="task_save_wod",
    ignore_result=True
)
def task_save_wod():
    save_wod(CROSSFIT_WOD_URL, CRAWLER_START_DATE)
    logger.info("Saved WOD")
