from abc import ABC, abstractmethod

from schemas import PublicationSchema
from utils.types import PublicationType
from utils.regex import clean_url_and_get_content_type

from ..validators import IValidate
from ..validators.base import ValidationMode
from ..repo import IPublicationRepo
from .entries import PublicationData


class ICreatePublication(ABC):
    @abstractmethod
    def __call__(self, user_id: int, schema: PublicationSchema) -> PublicationType:
        ...


class CreatePublication(ICreatePublication):
    def __init__(self, repo: IPublicationRepo, validate_url: IValidate) -> None:
        self.repo = repo
        self.validate_url = validate_url

    def __call__(self, user_id: int, schema: PublicationSchema) -> PublicationType:
        schema = self._clean(schema)
        self._validate(schema)
        schema = self._to_entry(schema)
        return self._create(user_id, schema)

    def _clean(self, schema: PublicationSchema) -> PublicationSchema:
        schema.url = str(schema.url)
        return schema

    def _validate(self, schema: PublicationSchema) -> None:
        self.validate_url(schema.url, mode=ValidationMode.OR, raise_exception=True)

    def _to_entry(self, schema: PublicationSchema) -> PublicationData:
        url, type = clean_url_and_get_content_type(schema.url)
        return PublicationData(url=url, type=type)

    def _create(self, user_id: int, entry: PublicationData) -> PublicationType:
        return self.repo.create(user_id, entry)
