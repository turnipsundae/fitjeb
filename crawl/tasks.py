from celery.task.schedules import crontab
from celery.decorators import task, periodic_task
from celery.utils.log import get_task_logger

from crawl.utils import save_latest_wod, save_old_wod

from crawl.settings import CRAWLER_FREQ_MINUTE, CRAWLER_FREQ_HOUR, CRAWLER_START_DATE

logger = get_task_logger(__name__)

@task(name="task_save_latest_wod")
def task_save_latest_wod():
    """
    Saves latest wod from Crossfit.com
    """
    # save_latest_wod()
    logger.info("Saved WOD from Crossfit.com")

@periodic_task(
    run_every=(crontab(minute=CRAWLER_FREQ_MINUTE, hour=CRAWLER_FREQ_HOUR)),
    name="task_save_specific_wod",
    ignore_result=True
)
def task_save_specific_wod():
    """
    Saves WOD from Crossfit.com beginning from stt art date,
    and skipping past any previously crawled dates.
    """
    # save_old_wod(CRAWLER_START_DATE)
    logger.info("Saved WOD from Crossfit.com")
