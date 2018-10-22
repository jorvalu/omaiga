import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aggregator.settings')

app = Celery('aggregator')
app.config_from_object('django.conf:settings')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'rank_all': {
        'task': 'links.tasks.rank_all',
        'schedule': 10,
    },
}
