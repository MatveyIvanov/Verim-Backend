from abc import ABC, abstractmethod


class IPasswordValidator(ABC):

    @abstractmethod
    def __call__(self, password: str) -> None: ...


class PasswordValidator(IPasswordValidator):

    def __call__(self, password: str) -> None:
        return
