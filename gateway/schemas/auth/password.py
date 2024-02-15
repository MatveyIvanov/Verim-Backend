from pydantic.dataclasses import dataclass
from pydantic import EmailStr, Field

from config import settings


@dataclass
class ChangePasswordSchema:
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=1)
    re_new_password: str = Field(min_length=1)


@dataclass
class ResetPasswordSchema:
    email: EmailStr = Field(min_length=1)


@dataclass
class ResetPasswordConfirmSchema:
    email: EmailStr = Field(min_length=1)
    code: str = Field(
        min_length=settings.CONFIRMATION_CODE_LENGTH,
        max_length=settings.CONFIRMATION_CODE_LENGTH,
    )
    new_password: str = Field(min_length=1)
    re_new_password: str = Field(min_length=1)
