from abc import ABC, abstractmethod

from ..validators import IValidate
from ..password import IHashPassword
from ..repo import IUserRepo
from ..codes import ICreateCode
from ..codes.types import CodeTypeEnum
from config.i18n import _
from config.settings import CONFIRM_EMAIL_CHECK_DELAY
from schemas import RegistrationSchema, CodeSentSchema
from utils.types import UserType
from utils.exceptions import Custom400Exception
from utils.time import get_current_time_with_delta


class IRegisterUser(ABC):
    @abstractmethod
    def __call__(self, entry: RegistrationSchema) -> CodeSentSchema:
        ...


class RegisterUser(IRegisterUser):
    def __init__(
        self,
        create_code: ICreateCode,
        validate_username: IValidate,
        validate_password: IValidate,
        hash_password: IHashPassword,
        repo: IUserRepo,
    ) -> None:
        self.create_code = create_code
        self.validate_username = validate_username
        self.validate_password = validate_password
        self.hash_password = hash_password
        self.repo = repo

    def __call__(self, entry: RegistrationSchema) -> CodeSentSchema:
        self._validate_email(entry)
        self._validate_username(entry)
        self._validate_password(entry)
        entry.password = self._hash_password(entry)
        user = self._create_user(entry)
        self._send_registration_check_task(user)
        return self._create_code(user)

    def _validate_email(self, entry: RegistrationSchema) -> None:
        if self.repo.email_exists(entry.email):
            raise Custom400Exception(_("Email is already taken."))

    def _validate_username(self, entry: RegistrationSchema) -> None:
        self.validate_username(entry.username, raise_exception=True)
        if self.repo.username_exists(entry.username):
            raise Custom400Exception(_("Username is already taken."))

    def _validate_password(self, entry: RegistrationSchema) -> None:
        if entry.password != entry.re_password:
            raise Custom400Exception(_("Password mismatch."))
        self.validate_password(entry.password, raise_exception=True)

    def _create_user(self, entry: RegistrationSchema) -> UserType:
        return self.repo.create(entry)

    def _hash_password(self, entry: RegistrationSchema) -> None:
        return self.hash_password(entry.password)

    def _send_registration_check_task(self, user: UserType) -> None:
        from config.celery import app as celery_app

        celery_app.send_task(
            "config.celery.ckeck_email_confirmed",
            args=(user.id,),
            eta=get_current_time_with_delta(seconds=CONFIRM_EMAIL_CHECK_DELAY),
        )

    def _create_code(self, user: UserType) -> CodeSentSchema:
        return self.create_code(user, CodeTypeEnum.EMAIL_CONFIRM, send=True)
