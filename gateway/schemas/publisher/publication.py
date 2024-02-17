from typing import List
from enum import Enum

from pydantic.dataclasses import dataclass
from pydantic import HttpUrl


class ContentType(str, Enum):
    YOUTUBE = "YOUTUBE"
    VK = "VK"
    TIKTOK = "TIKTOK"
    TWITCH = "TWITCH"


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
    created_at: str
    believed: bool | None


@dataclass
class PublicationSelectionSchema:
    items: List[PublicationSchema]
    total: int
    page: int
    size: int
    pages: int
