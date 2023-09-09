from pydantic.dataclasses import dataclass


@dataclass
class JWTTokensSchema:
    access: str
    refresh: str
