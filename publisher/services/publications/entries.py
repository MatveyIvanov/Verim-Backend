from dataclasses import dataclass

from ..entries import ContentType


@dataclass
class PublicationData:
    url: str
    type: ContentType
