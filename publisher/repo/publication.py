from dataclasses import asdict

from sqlalchemy import and_, func
from sqlalchemy.orm import Query, contains_eager
from fastapi_pagination.ext.sqlalchemy import paginate

from models.publication import Publication
from models.vote import Vote
from services.repo import IPublicationRepo
from schemas.publication import PublicationSchema
from services.publications.entries import CreatePublicationData
from utils.repo import pagination_transformer
from utils.types import PublicationType


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

    def selection(self, user_id: int | None) -> Query[Publication]:
        with self.session_factory() as session:
            return paginate(
                session.query(
                    self.model.id,
                    self.model.url,
                    self.model.type,
                    self.model.believed_count,
                    self.model.disbelieved_count,
                    self.model.created_at,
                    Vote.believed,
                )
                .outerjoin(
                    Vote,
                    and_(Vote.publication_id == self.model.id, Vote.user_id == user_id),
                )
                .add_columns(Vote.believed),
                transformer=pagination_transformer(PublicationSchema),
            )
