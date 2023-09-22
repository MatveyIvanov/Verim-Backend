from typing import Dict

from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from schemas import RegistrationSchema
from services.repo import IUserRepo
from models.users import User
from utils.types import UserType


class UserRepo(IUserRepo):
    model = User

    def all(
        self,
        *,
        session: Session | None = None,
        include_not_confirmed_email: bool = False
    ):
        with session or self.session_factory() as session:
            qs = session.query(self.model)
            if not include_not_confirmed_email:
                qs = qs.filter(self.model.email_confirmed == True)
            return qs

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
                self.all(session=session, include_not_confirmed_email=True)
                .exists()
                .where(func.lower(self.model.email) == func.lower(email))
            ).scalar()

    def username_exists(self, username: str) -> bool:
        with self.session_factory() as session:
            return session.query(
                self.all(session=session, include_not_confirmed_email=True)
                .exists()
                .where(func.lower(self.model.username) == func.lower(username))
            ).scalar()

    def get_by_login(self, login: str) -> UserType | None:
        return (
            self.all()
            .filter(
                or_(
                    func.lower(self.model.username) == func.lower(login),
                    func.lower(self.model.email) == func.lower(login),
                )
            )
            .first()
        )

    def get_by_id(self, id: int) -> UserType | None:
        return (
            self.all(include_not_confirmed_email=True)
            .filter(self.model.id == id)
            .first()
        )

    def get_by_email(self, email: str) -> UserType | None:
        return (
            self.all()
            .filter(
                func.lower(self.model.email) == func.lower(email),
            )
            .first()
        )
