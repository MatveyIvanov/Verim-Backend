from abc import ABC, abstractmethod

from schemas import CreatePublicationSchema
from utils.types import PublicationType
from utils.regex import clean_url_and_get_content_type

from ..validators import IValidate
from ..validators.base import ValidationMode
from ..repo import IPublicationRepo
from .entries import CreatePublicationData, PublicationData


class ICreatePublication(ABC):
    @abstractmethod
    def __call__(
        self, user_id: int, schema: CreatePublicationSchema
    ) -> PublicationData:
        ...


class CreatePublication(ICreatePublication):
    def __init__(self, repo: IPublicationRepo, validate_url: IValidate) -> None:
        self.repo = repo
        self.validate_url = validate_url

    def __call__(
        self, user_id: int, schema: CreatePublicationSchema
    ) -> PublicationData:
        schema = self._clean(schema)
        self._validate(schema)
        schema = self._to_entry(schema)
        publication = self._create(user_id, schema)
        return self._to_schema(publication)

    def _clean(self, schema: CreatePublicationSchema) -> CreatePublicationSchema:
        schema.url = str(schema.url)
        return schema

    def _validate(self, schema: CreatePublicationSchema) -> None:
        self.validate_url(schema.url, mode=ValidationMode.OR, raise_exception=True)

    def _to_entry(self, schema: CreatePublicationSchema) -> CreatePublicationData:
        url, type = clean_url_and_get_content_type(schema.url)
        return CreatePublicationData(url=url, type=type)

    def _create(self, user_id: int, entry: CreatePublicationData) -> PublicationType:
        return self.repo.create(user_id, entry)

    def _to_schema(self, publication: PublicationType) -> PublicationData:
        return PublicationData(
            id=publication.id,
            url=publication.url,
            type=publication.type,
            believed_count=publication.believed_count,
            disbelieved_count=publication.disbelieved_count,
            created_at=str(publication.created_at),
        )
