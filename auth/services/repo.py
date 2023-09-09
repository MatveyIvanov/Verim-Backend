from abc import abstractmethod

from schemas import RegistrationSchema
from utils.typing import UserType
from utils.repo import IRepo


class IUserRepo(IRepo):
    @abstractmethod
    def create(self, entry: RegistrationSchema) -> UserType:
        ...

    @abstractmethod
    def update(self, user: UserType) -> None:
        ...

    @abstractmethod
    def email_exists(self, email: str) -> bool:
        ...

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        ...

    @abstractmethod
    def get_by_login(self, login: str) -> UserType | None:
        ...
