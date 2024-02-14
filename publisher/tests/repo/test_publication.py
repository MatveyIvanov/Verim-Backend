import pytest

from config.di import get_di_test_container
from services.repo import IPublicationRepo
from services.publications.entries import CreatePublicationData, ContentType
from utils.test import RepoTestMixin


container = get_di_test_container()


class TestPublicationRepo(RepoTestMixin):
    repo: IPublicationRepo = container.publication_repo()

    def setup_method(self):
        self.entry = CreatePublicationData(
            url="https://example.com", type=ContentType.YOUTUBE
        )

    def test_create(self):
        self.repo.create(1, self.entry)

    def test_selection_no_vote(self):
        pass
