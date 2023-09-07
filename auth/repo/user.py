from dataclasses import asdict

from schemas.register import RegistrationSchema
from services.repo import IUserRepo
from models.users import User
from utils.typing import UserType


class UserRepo(IUserRepo):
    model = User

    def create(self, entry: RegistrationSchema) -> UserType:
        user = self.model(
            email=entry.email,
            username=entry.username
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: UserType) -> UserType:
        self.db.commit()
        self.db.refresh(user)
        return user
