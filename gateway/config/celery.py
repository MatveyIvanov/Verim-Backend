from asgiref.sync import async_to_sync
from celery import Celery

from .mail import SendEmailDict


app = Celery("celery_app")
app.config_from_object("config.celery_config")
app.autodiscover_tasks()


@app.task
def send_email(entry_dict: SendEmailDict) -> None:
    from .di import Container

    async_to_sync(Container()._send_email())(entry_dict)


@app.task
def check_email_confirmed(user_id: int) -> bool | None:
    from .di import Container

    return Container().check_registration()(user_id)  # FIXME: вызывать grpc
