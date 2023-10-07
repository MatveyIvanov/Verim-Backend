from pydantic.dataclasses import dataclass
from pydantic import EmailStr


@dataclass
class ChangePasswordSchema:
    current_password: str
    new_password: str
    re_new_password: str


@dataclass
class ResetPasswordSchema:
    email: EmailStr
