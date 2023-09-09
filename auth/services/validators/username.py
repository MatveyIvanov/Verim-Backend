from .base import LengthValidator, CharactersValidator


class UsernameLengthValidator(LengthValidator):
    error_messages = {
        "min_length": lambda min_length: "Make sure that username length is not less than %(min_length)s."
        % {"min_length": min_length},
        "max_length": lambda max_length: "Make sure that username length is not greater than %(max_length)s."
        % {"max_length": max_length},
    }


class UsernameCharactersValidator(CharactersValidator):
    error_messages = {
        "invalid_characters": lambda invalid_characters: "Invalid characters in username: %(invalid_characters)s."
        % {"invalid_characters": ", ".join(invalid_characters)}
    }
