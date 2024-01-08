import re
from abc import ABC, abstractmethod
from typing import Any, Pattern

from config.i18n import _
from utils.exceptions import Custom400Exception


class IValidate(ABC):
    @abstractmethod
    def __call__(self, data: Any, *, raise_exception: bool = True) -> bool:
        ...


class IValidator(ABC):
    @abstractmethod
    def is_valid(self, data: Any, raise_exception: bool) -> bool:
        ...


class Validate(IValidate):
    def __init__(self, *validators: IValidator):
        self.validators = validators

    def __call__(self, data: Any, *, raise_exception: bool = True) -> None:
        is_valid = True
        for validator in self.validators:
            is_valid = validator.is_valid(data, raise_exception)

        return is_valid


class RegexValidator(IValidator):
    error_messages = {"no_match": _("Given string do not match specified pattern.")}

    def __init__(self, pattern: Pattern) -> None:
        self.pattern = pattern

    def is_valid(self, data: Any, raise_exception: bool = True) -> bool:
        is_valid = True
        if re.match(self.pattern, data) is None:
            if raise_exception:
                raise Custom400Exception(self.error_messages["no_match"])
            is_valid = False
        return is_valid
