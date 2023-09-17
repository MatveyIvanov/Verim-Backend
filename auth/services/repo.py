from abc import abstractmethod
from typing import Dict

from schemas import RegistrationSchema
from utils.types import UserType
from utils.repo import IRepo


class IUserRepo(IRepo):
    @abstractmethod
    def create(self, entry: RegistrationSchema) -> UserType:
        ...

    @abstractmethod
    def update(self, user: UserType, values: Dict) -> None:
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

    @abstractmethod
    def get_by_id(self, id: int) -> UserType | None:
        ...
