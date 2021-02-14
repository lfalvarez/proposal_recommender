import os

from celery import Celery
import time

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "config.settings.local")

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def send_mails_to(self, recommendation):
    for recommendation_for_candidate in recommendation.recommendations_for_candidate.all():
        recommendation_for_candidate.send()
        time.sleep(1)
