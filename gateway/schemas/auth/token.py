from pydantic.dataclasses import dataclass
from pydantic import Field


@dataclass
class JWTTokensSchema:
    access: str
    refresh: str


@dataclass
class RefreshTokensSchema:
    refresh: str = Field(min_length=1)
