from abc import abstractmethod

from sqlalchemy.orm import Query

from models.publication import Publication
from utils.repo import IRepo
from utils.types import PublicationType

from .publications.entries import CreatePublicationData


class IPublicationRepo(IRepo):
    @abstractmethod
    def create(self, user_id: int, entry: CreatePublicationData) -> PublicationType:
        ...

    @abstractmethod
    def selection(self, user_id: int | None) -> Query[Publication]:
        ...


class IVoteRepo(IRepo):
    pass
