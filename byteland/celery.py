import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# from byteland.story.tasks import task_update_story_rank


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'byteland.settings')
app = Celery('byteland')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s("world"), expires=10)

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'byteland.celery.test',
        'schedule': 30.0,
        'args': ("Hello world!")
    },
}


@app.task
def test(arg):
    print(arg)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
