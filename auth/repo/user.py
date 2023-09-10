from typing import Dict, Optional

from sqlalchemy import func, or_

from schemas import RegistrationSchema
from services.repo import IUserRepo
from models.users import User
from utils.typing import UserType


class UserRepo(IUserRepo):
    model = User

    def create(self, entry: RegistrationSchema) -> UserType:
        user = self.model(
            email=entry.email.lower(), username=entry.username, password=entry.password
        )
        with self.session_factory() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
        return user

    def update(self, user: UserType, values: Dict) -> UserType:
        with self.session_factory() as session:
            session.query(self.model).filter(self.model.id == user.id).update(values)
            session.commit()
        return user

    def email_exists(self, email: str) -> bool:
        with self.session_factory() as session:
            return session.query(
                session.query(self.model)
                .exists()
                .where(func.lower(self.model.email) == func.lower(email))
            ).scalar()

    def username_exists(self, username: str) -> bool:
        with self.session_factory() as session:
            return session.query(
                session.query(self.model)
                .exists()
                .where(func.lower(self.model.username) == func.lower(username))
            ).scalar()

    def get_by_login(self, login: str) -> UserType | None:
        with self.session_factory() as session:
            return (
                session.query(self.model)
                .filter(
                    or_(
                        func.lower(self.model.username) == func.lower(login),
                        func.lower(self.model.email) == func.lower(login),
                    )
                )
                .first()
            )

    def get_by_id(self, id: int) -> UserType | None:
        with self.session_factory() as session:
            return session.query(self.model).filter(self.model.id == id).first()
