from abc import abstractmethod

from .types import CodeType
from ..entries import CreateCodeEntry
from utils.repo import IRepo


class ICodeRepo(IRepo):
    @abstractmethod
    def create(self, entry: CreateCodeEntry) -> CodeType:
        ...

    @abstractmethod
    def get_last(self, user_id: int, type: CodeType) -> CodeType | None:
        ...
