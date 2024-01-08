from abc import abstractmethod

from utils.repo import IRepo
from utils.types import PublicationType

from .publications.entries import PublicationData


class IPublicationRepo(IRepo):
    @abstractmethod
    def create(self, user_id: int, entry: PublicationData) -> PublicationType:
        ...
