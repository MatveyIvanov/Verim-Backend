from pydantic.dataclasses import dataclass
from pydantic import HttpUrl


@dataclass
class PublicationSchema:
    url: HttpUrl
