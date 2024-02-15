from pydantic import EmailStr, Field
from pydantic.dataclasses import dataclass

from config import settings


@dataclass
class RegistrationSchema:
    email: EmailStr = Field(min_length=1)
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    re_password: str = Field(min_length=1)


@dataclass
class CodeSentSchema:
    email: EmailStr
    message: str


@dataclass
class ConfirmRegistrationSchema:
    email: EmailStr = Field(min_length=1)
    code: str = Field(
        min_length=settings.CONFIRMATION_CODE_LENGTH,
        max_length=settings.CONFIRMATION_CODE_LENGTH,
    )


@dataclass
class RepeatRegistrationCodeSchema:
    email: EmailStr = Field(min_length=1)
