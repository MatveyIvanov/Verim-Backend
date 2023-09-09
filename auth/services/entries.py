from dataclasses import dataclass


@dataclass
class PasswordRequiredCharactersGroup:
    name: str
    characters: str
    description: str
