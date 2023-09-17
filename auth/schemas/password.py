from pydantic.dataclasses import dataclass


@dataclass
class ChangePasswordSchema:
    current_password: str
    new_password: str
    re_new_password: str
