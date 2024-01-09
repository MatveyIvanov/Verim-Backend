from datetime import datetime

from pydantic.dataclasses import dataclass
from pydantic import HttpUrl
from pydantic.fields import Field

from services.entries import ContentType


@dataclass
class CreatePublicationSchema:
    url: HttpUrl


@dataclass
class PublicationSchema:
    id: int
    url: str
    type: ContentType
    believed_count: int
    disbelieved_count: int
    created_at: datetime
    believed: bool | None
