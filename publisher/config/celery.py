from asgiref.sync import async_to_sync
from celery import Celery

from .mail import SendEmailDict
from .di import Container


app = Celery("celery_app")
app.config_from_object("config.celery_config")
app.autodiscover_tasks()
