from typing import Dict

import pytest
import mock

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


class RepoTestMixin:
    repo: IRepo = None
