import asyncio

from asgiref.sync import async_to_sync
from celery import Celery

from .mail import SendEmailDict
from auth_grpc_typed import CheckEmailConfirmedRequest
from config.di import Container


app = Celery("celery_app")
app.config_from_object("config.celery_config")
app.autodiscover_tasks()


@app.task
def send_email(entry_dict: SendEmailDict) -> None:
    async_to_sync(Container()._send_email())(entry_dict)


@app.task
def check_email_confirmed(user_id: int) -> bool | None:
    loop = asyncio.get_event_loop()
    coro = (
        Container()
        .auth_grpc()
        .check_email_confirmed(request=CheckEmailConfirmedRequest(user_id=user_id))
    )
    return loop.run_until_complete(coro).confirmed
