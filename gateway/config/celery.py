from asgiref.sync import async_to_sync
from celery import Celery

from .mail import SendEmailDict
from .di import Container


app = Celery("celery_app")
app.config_from_object("config.celery_config")
app.autodiscover_tasks()


@app.task
def send_email(entry_dict: SendEmailDict) -> None:
    async_to_sync(Container()._send_email())(entry_dict)


@app.task
def ckeck_email_confirmed(user_id: int) -> bool | None:
    return Container().check_registration()(user_id)
