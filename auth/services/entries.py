from dataclasses import dataclass
from datetime import datetime


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
