from abc import ABC, abstractmethod

from schemas import VoteSchema
from services.repo import IVoteRepo
from utils.types import VoteType


class IVote(ABC):
    @abstractmethod
    def __call__(self, user_id: int, publication_id: int, schema: VoteSchema) -> None:
        ...


class Vote(IVote):
    def __init__(self, repo: IVoteRepo) -> None:
        self.repo = repo

    def __call__(self, user_id: int, publication_id: int, schema: VoteSchema) -> None:
        vote = self._get(user_id, publication_id)
        if vote:
            self._update(vote, schema)
        else:
            self._create(user_id, publication_id, schema)

    def _get(self, user_id: int, publication_id: int) -> VoteType | None:
        return self.repo.get(user_id, publication_id)

    def _create(
        self, user_id: int, publication_id: int, schema: VoteSchema
    ) -> VoteType:
        return self.repo.create(user_id, publication_id, schema.believed)

    def _update(self, vote: VoteType, schema: VoteSchema) -> None:
        self.repo.update(vote.id, schema.believed)
