from abc import ABC, abstractmethod
import hashlib

from .repo import IUserRepo
from config import settings
from utils.typing import UserType
from utils.random import get_random_string


class ISetPassword(ABC):

    @abstractmethod
    def __call__(self, user: UserType, password: str) -> UserType: ...


class SetPassword(ISetPassword):

    def __init__(self, repo: IUserRepo) -> None:
        self.repo = repo

    def __call__(self, user: UserType, password: str) -> UserType:
        user.password = self._hash_password(password)
        return self.repo.update(user)

    def _hash_password(self, password: str) -> str:
        return hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode(),
            salt=get_random_string(settings.PASSWORD_SALT_LENGTH).encode(),
            iterations=settings.PASSWORD_HASH_ITERATIONS
        )
