import os 
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myshop.settings")


app = Celery("myshop")

app.config_from_object("django.conf:settings",namespace="CELERY")

app.autodiscover_tasks()


app.conf.beat_schedule = {
    
    'send-mail-every-day-at-8': {
        'task': 'shop.tasks.send_notification_email',
        'schedule':  crontab(minute="*"),
       
    },
}