from typing import Dict

from sqlalchemy import func

from schemas.register import RegistrationSchema
from services.repo import IUserRepo
from models.users import User
from utils.typing import UserType


class UserRepo(IUserRepo):
    model = User

    def create(self, entry: RegistrationSchema) -> UserType:
        user = self.model(
            email=entry.email, username=entry.username, password=entry.password
        )
        with self.session_factory() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    def update(self, user: UserType, values: Dict) -> UserType:
        with self.session_factory() as session:
            session.query(User).filter(User.id == user.id).update(values)
            session.commit()
        return user

    def email_exists(self, email: str) -> bool:
        with self.session_factory() as session:
            return session.query(
                session.query(User)
                .exists()
                .where(func.lower(User.email) == func.lower(email))
            ).scalar()

    def username_exists(self, username: str) -> bool:
        with self.session_factory() as session:
            return session.query(
                session.query(User)
                .exists()
                .where(func.lower(User.username) == func.lower(username))
            ).scalar()
