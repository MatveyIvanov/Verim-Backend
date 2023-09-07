from abc import ABC, abstractmethod

from schemas.register import (
    RegistrationSchema,
    JWTTokensSchema
)
from ..validators import (
    IPasswordValidator,
    IUsernameValidator,
)
from ..jwt import (
    ICreateJWTTokens,
)
from ..password import ISetPassword
from ..repo import IUserRepo
from utils.typing import UserType


class IRegisterUser(ABC):

    @abstractmethod
    def __call__(self, entry: RegistrationSchema) -> JWTTokensSchema: ...


class RegisterUser(IRegisterUser):

    def __init__(
        self,
        create_jwt_tokens: ICreateJWTTokens,
        username_validator: IUsernameValidator,
        password_validator: IPasswordValidator,
        set_password: ISetPassword,
        repo: IUserRepo
    ) -> None:
        self.create_jwt_tokens = create_jwt_tokens
        self.username_validator = username_validator
        self.password_validator = password_validator
        self.set_password = set_password
        self.repo = repo

    def __call__(self, entry: RegistrationSchema) -> JWTTokensSchema:
        self._validate_email(entry)
        self._validate_username(entry)
        self._validate_password(entry)
        user = self._create_user(entry)
        user = self._set_password(user, entry)
        return self._make_tokens(user)

    def _validate_email(self, entry: RegistrationSchema) -> None:
        pass

    def _validate_username(self, entry: RegistrationSchema) -> None:
        self.username_validator(entry.username)

    def _validate_password(self, entry: RegistrationSchema) -> None:
        self.password_validator(entry.password)

    def _create_user(self, entry: RegistrationSchema) -> UserType:
        return self.repo.create(entry)

    def _set_password(self, user: UserType, entry: RegistrationSchema) -> None:
        return self.set_password(user, entry.password)

    def _make_tokens(self, user: UserType) -> JWTTokensSchema:
        return self.create_jwt_tokens(user)
