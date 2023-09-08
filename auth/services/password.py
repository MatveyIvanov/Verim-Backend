from abc import ABC, abstractmethod
import hashlib

from config import settings
from utils.random import get_random_string


class IHashPassword(ABC):

    @abstractmethod
    def __call__(self, password: str) -> str: ...


class HashPassword(IHashPassword):

    def __call__(self, password: str) -> str:
        return hashlib.pbkdf2_hmac(
            hash_name='sha256',
            password=password.encode(),
            salt=get_random_string(settings.PASSWORD_SALT_LENGTH).encode(),
            iterations=settings.PASSWORD_HASH_ITERATIONS
        ).hex()
