from pydantic import (
    EmailStr,
)
from pydantic.dataclasses import dataclass


@dataclass
class LoginSchema:
    login: str | EmailStr
    password: str
