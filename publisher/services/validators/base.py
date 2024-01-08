import re
from abc import ABC, abstractmethod
from typing import Any, Pattern
from enum import Enum

from config.i18n import _
from utils.exceptions import Custom400Exception


class ValidationMode(Enum):
    OR = "OR"
    AND = "AND"


class IValidate(ABC):
    @abstractmethod
    def __call__(
        self,
        data: Any,
        *,
        mode: ValidationMode = ValidationMode.AND,
        raise_exception: bool = True
    ) -> bool:
        ...


class IValidator(ABC):
    @abstractmethod
    def is_valid(self, data: Any, raise_exception: bool) -> bool:
        ...


class Validate(IValidate):
    def __init__(self, *validators: IValidator):
        self.validators = validators

    def __call__(
        self,
        data: Any,
        *,
        mode: ValidationMode = ValidationMode.AND,
        raise_exception: bool = True
    ) -> None:
        is_valid = True
        for validator in self.validators:
            is_valid = validator.is_valid(data, raise_exception)
            if mode == ValidationMode.AND and not is_valid:
                return is_valid
            if mode == ValidationMode.OR and is_valid:
                return is_valid
        return is_valid
