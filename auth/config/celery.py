from asgiref.sync import async_to_sync
from celery import Celery
from dependency_injector.wiring import Provide, inject

from .mail import SendEmailDict, _ISendEmail
from .di import Container


app = Celery("celery_app")
app.config_from_object("config.celery_config")
app.autodiscover_tasks()

Container().wire(modules=[__name__])


@app.task
@inject
def send_email(
    entry_dict: SendEmailDict, service: _ISendEmail = Provide[Container._send_email]
) -> None:
    async_to_sync(Container()._send_email())(entry_dict)


@app.task
@inject
def ckeck_email_confirmed(self, user_id: int) -> None:
    pass
