from abc import ABC, abstractmethod

from ..entries import SendCodeEntry
from .types import CodeTypeEnum
from config.mail import ISendEmail, SendEmailEntry
from config.i18n import _
from schemas import CodeSentSchema


class ISendCode(ABC):
    @abstractmethod
    def __call__(self, entry: SendCodeEntry) -> CodeSentSchema:
        ...


class SendCode(ISendCode):
    subject_map = {CodeTypeEnum.EMAIL_CONFIRM.value: _("Email confirmation")}
    message_map = {
        CodeTypeEnum.EMAIL_CONFIRM.value: _("Your confirmation code: %(code)s")
    }
    result_map = {
        CodeTypeEnum.EMAIL_CONFIRM.value: _("Code successfully sent to %(email)s.")
    }

    def __init__(self, send_email: ISendEmail) -> None:
        self.send_email = send_email

    def __call__(self, entry: SendCodeEntry) -> CodeSentSchema:
        self._send_email(entry)
        return self._result(entry)

    def _send_email(self, entry: SendCodeEntry) -> None:
        self.send_email(
            entry=SendEmailEntry(
                emails=[entry.email],
                subject=self.subject_map[entry.type],
                message=self.message_map[entry.type] % {"code": entry.code},
            )
        )

    def _result(self, entry: SendCodeEntry) -> CodeSentSchema:
        return CodeSentSchema(
            email=entry.email,
            message=self.result_map[entry.type] % {"email": entry.email},
        )
