from abc import ABC, abstractmethod


class IUsernameValidator(ABC):

    @abstractmethod
    def __call__(self, username: str) -> None: ...


class UsernameValidator(IUsernameValidator):

    def __call__(self, password: str) -> None:
        return

