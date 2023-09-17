from dataclasses import dataclass
from datetime import datetime

from .codes.types import CodeType


@dataclass
class PasswordRequiredCharactersGroup:
    name: str
    characters: str
    description: str


@dataclass
class JWTPayload:
    user: int
    exp: datetime
    created_at: datetime


@dataclass
class CreateCodeEntry:
    user_id: int
    code: str
    type: CodeType
