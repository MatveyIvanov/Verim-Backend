from abc import abstractmethod

from schemas.register import RegistrationSchema
from utils.typing import UserType
from utils.repo import IRepo


class IUserRepo(IRepo):

    @abstractmethod
    def create(self, entry: RegistrationSchema) -> UserType: ...

    @abstractmethod
    def update(self, user: UserType) -> None: ...
