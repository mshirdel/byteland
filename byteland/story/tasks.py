# from celery.task.schedules import crontab
from celery.decorators import task
from celery.utils.log import get_task_logger

from byteland.story.models import Story

logger = get_task_logger(__name__)


# @periodic_task(
#     run_every=(crontab(hour='*/5')),
#     name="update_all_stories_rank",
#     ignore_result=True
# )
@task(name="task_update_story_rank")
def task_update_story_rank():
    for s in Story.stories.all():
        s.calc_rank()
    logger.info("Update all stories ranks")
