from typing import Dict
from types import SimpleNamespace

import pytest

from config import settings
from utils.repo import IRepo


class SchemaTestMixin:
    schema_class = None

    def assertValid(self, data: Dict) -> None:
        self.schema_class(**data)

    def assertNotValid(self, data: Dict) -> None:
        with pytest.raises(ValueError):
            self.schema_class(**data)


class ServiceTestMixin:
    service = None
    user = SimpleNamespace(
        **{
            "id": 1,
            "login": "testuser",
            "password": "testpassword",
        }
    )


def environment_safe_repo_test(func):
    """
    Декоратор предотвращает выполнение тестов репозиториев,
    если `TESTING_REPO_ALLOWED = False`
    """

    def wrapper(*args, **kwargs):
        if not settings.TESTING_REPO_ALLOWED:
            return
        return func(*args, **kwargs)

    return wrapper


class RepoTestMixin:
    repo: IRepo = None
