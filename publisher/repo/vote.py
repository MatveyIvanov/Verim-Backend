from services.repo import IVoteRepo
from models.vote import Vote


class VoteRepo(IVoteRepo):
    model = Vote
