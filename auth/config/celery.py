from celery import Celery
from dependency_injector.wiring import Provide, inject

from .mail import SendEmailDict, _ISendEmail
from .di import Container


app = Celery("celery_app")
app.config_from_object("config.celery_config")
app.autodiscover_tasks()


@app.task
@inject
def send_email(
    entry_dict: SendEmailDict, service: _ISendEmail = Provide[Container._send_email]
):
    service(entry_dict)
