from dataclasses import asdict

from models.publication import Publication
from services.repo import IPublicationRepo
from utils.types import PublicationType

from services.publications.entries import CreatePublicationData


class PublicationRepo(IPublicationRepo):
    model = Publication

    def create(self, user_id: int, entry: CreatePublicationData) -> PublicationType:
        entry.type = entry.type.value
        publication = self.model(user_id=user_id, **asdict(entry))
        with self.session_factory() as session:
            session.add(publication)
            session.commit()
            session.refresh(publication)
        return publication
