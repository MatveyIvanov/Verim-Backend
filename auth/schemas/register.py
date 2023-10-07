from pydantic import EmailStr, Field
from pydantic.dataclasses import dataclass


@dataclass
class RegistrationSchema:
    email: EmailStr
    username: str
    password: str
    re_password: str


@dataclass
class CodeSentSchema:
    email: EmailStr
    message: str


@dataclass
class ConfirmRegistrationSchema:
    email: EmailStr
    code: str = Field(min_length=4, max_length=4)


@dataclass
class RepeatRegistrationCodeSchema:
    email: EmailStr
