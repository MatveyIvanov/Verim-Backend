from abc import ABC, abstractmethod

import bcrypt


ENCODING = "utf-8"


class IHashPassword(ABC):
    @abstractmethod
    def __call__(self, password: str) -> str:
        ...


class ICheckPassword(ABC):
    @abstractmethod
    def __call__(self, plain_pwd: str, hashed_pwd: str) -> bool: ...


class HashPassword(IHashPassword):
    def __call__(self, password: str) -> str:
        return bcrypt.hashpw(password.encode(ENCODING), bcrypt.gensalt()).decode(ENCODING)


class CheckPassword(ICheckPassword):

    def __call__(self, plain_pwd: str, hashed_pwd: str) -> bool:
        return bcrypt.checkpw(plain_pwd.encode(ENCODING), hashed_pwd.encode(ENCODING))
