from abc import ABC, abstractmethod

from .create import ICreateJWTTokens
from schemas import JWTTokensSchema, RefreshTokensSchema
from utils.types import UserType
from utils.middleware import authenticate_by_token


class IRefreshJWTTokens(ABC):
    @abstractmethod
    def __call__(self, entry: RefreshTokensSchema) -> JWTTokensSchema: ...


class RefreshJWTTokens(IRefreshJWTTokens):
    def __init__(self, create_jwt_tokens: ICreateJWTTokens) -> None:
        self.create_jwt_tokens = create_jwt_tokens

    def __call__(self, entry: RefreshTokensSchema) -> JWTTokensSchema:
        return self.create_jwt_tokens(user=self._get_user(entry.refresh))

    def _get_user(self, refresh: str) -> UserType:
        return authenticate_by_token(refresh, access=False)
