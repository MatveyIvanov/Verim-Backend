from abc import ABC, abstractmethod
import string

from .types import CodeType, CodeTypeEnum
from ..entries import CreateCodeEntry
from .repo import ICodeRepo
from config import settings
from config.i18n import _
from utils.types import UserType
from utils.time import get_current_time
from utils.exceptions import Custom400Exception
from utils.random import get_random_string


class ICreateCode(ABC):
    @abstractmethod
    def __call__(self, user: UserType, type: CodeType) -> str:
        ...


class CreateCode(ICreateCode):
    def __init__(self, repo: ICodeRepo) -> None:
        self.repo = repo

    def __call__(self, user: UserType, type: CodeTypeEnum) -> str:
        self._check_has_active(user, type)
        return self._create_code(user, type).code

    def _check_has_active(self, user: UserType, type: CodeTypeEnum) -> None:
        last_code = self.repo.get_last(user.id, type)
        if not last_code:
            return

        seconds_diff = (get_current_time() - last_code.created_at).seconds
        if seconds_diff <= settings.CONFIRM_EMAIL_CODE_DURATION:
            raise Custom400Exception(
                _("New code will be available to obtain after: %(seconds)s")
                % {"seconds": settings.CONFIRM_EMAIL_CODE_DURATION - seconds_diff}
            )

    def _create_code(self, user: UserType, type: CodeTypeEnum) -> CodeType:
        return self.repo.create(
            entry=CreateCodeEntry(
                user_id=user.id,
                code=get_random_string(length=4, allowed_characters=string.digits),
                type=type,
            )
        )
