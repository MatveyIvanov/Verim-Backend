from smtplib import SMTPException
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import List

from fastapi_mail.config import ConnectionConfig
from fastapi_mail.schemas import MessageSchema, MessageType
from fastapi_mail import FastMail

from config import settings


__all__ = "SendEmailEntry"


config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    USE_CREDENTIALS=True,
    MAIL_SSL_TLS=False,
    MAIL_STARTTLS=True,
)


@dataclass
class SendEmailEntry:
    emails: List[str]
    subject: str
    message: str = ""


class ISendEmail(ABC):
    @abstractmethod
    def __call__(self, entry: SendEmailEntry) -> None:
        ...


class SendEmail(ISendEmail):
    async def __call__(self, entry: SendEmailEntry) -> None:
        await self._send_email(entry)

    async def _send_email(self, entry: SendEmailEntry) -> int:
        try:
            await FastMail(config).send_message(
                message=MessageSchema(
                    recipients=entry.emails,
                    subject=entry.subject,
                    body=entry.message,
                    subtype=MessageType.plain,
                )
            )
        except SMTPException as e:
            # logger.critical(f"Failed to send email - {e}", extra={'emails': entry.emails})
            raise Exception()
