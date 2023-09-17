from abc import ABC, abstractmethod

from schemas import ConfirmRegistrationSchema, JWTTokensSchema


class IConfirmRegistration(ABC):
    @abstractmethod
    def __call__(self, entry: ConfirmRegistrationSchema) -> JWTTokensSchema:
        ...


class ConfirmRegistration(IConfirmRegistration):
    def __init__(self, create_jwt_tokens, check_code, repo) -> None:
        self.create_jwt_tokens = create_jwt_tokens
        self.check_code = check_code
        self.repo = repo

    def __call__(self, entry: ConfirmRegistrationSchema) -> JWTTokensSchema:
        return super().__call__(entry)
