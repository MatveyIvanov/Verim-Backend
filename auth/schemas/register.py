from pydantic import (
    BaseModel,
    EmailStr,
)
from pydantic.dataclasses import dataclass


@dataclass
class RegistrationSchema:
    email: EmailStr
    username: str
    password: str
    re_password: str


@dataclass
class JWTTokensSchema:
    access: str
    refresh: str
