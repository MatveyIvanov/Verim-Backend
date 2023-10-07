from abc import ABC, abstractmethod

from ..repo import IUserRepo
from utils.types import UserType


class ICheckRegistration(ABC):
    @abstractmethod
    def __call__(self, user_id: int) -> bool | None:
        ...


class CheckRegistration(ICheckRegistration):
    def __init__(self, repo: IUserRepo) -> None:
        self.repo = repo

    def __call__(self, user_id: int) -> bool | None:
        user = self._get_user(user_id)
        if user is None:
            return None

        if not self._email_confirmed(user):
            self._delete_user(user)
            return False
        return True

    def _get_user(self, user_id: int) -> UserType | None:
        return self.repo.get_by_id(user_id)

    def _email_confirmed(self, user: UserType) -> bool:
        return user.email_confirmed

    def _delete_user(self, user: UserType) -> None:
        self.repo.delete(user)
