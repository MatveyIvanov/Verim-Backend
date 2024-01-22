from dataclasses import asdict

from services.repo import IVoteRepo
from models.vote import Vote
from utils.types import VoteType


class VoteRepo(IVoteRepo):
    model = Vote

    def get(self, user_id: int, publication_id: int) -> VoteType | None:
        with self.session_factory() as session:
            return (
                session.query(self.model)
                .filter(Vote.user_id == user_id, Vote.publication_id == publication_id)
                .first()
            )

    def create(
        self, user_id: int, publication_id: int, believed: bool | None
    ) -> VoteType:
        vote = self.model(
            user_id=user_id, publication_id=publication_id, believed=believed
        )
        with self.session_factory() as session:
            session.add(vote)
            session.commit()
            session.refresh(vote)
        return vote

    def update(self, vote_id: int, believed: bool | None) -> None:
        with self.session_factory() as session:
            session.query(self.model).filter(Vote.id == vote_id).update(
                {Vote.believed: believed}
            )
            session.commit()
