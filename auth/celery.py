import os
from celery import Celery
from django.conf import settings

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth.settings')

app = Celery('auth')
app.config_from_object('django.conf:settings')

app.conf.beat_schedule = {
    'send-email-once-a-week': {
        'task': 'users.tasks.task_send_email.task_to_send_email',
        'schedule': crontab(hour=12, minute=0, day_of_week=1)
    }
}


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

