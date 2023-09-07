from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class IMakeSession(ABC):

    @abstractmethod
    def __call__(self) -> Session: ...


class MakeSession(IMakeSession):

    def __call__(self) -> Session:
        from config.db import SessionLocal
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


class IRepo(ABC):
    db: Session

    def __init__(self, make_session: IMakeSession) -> None:
        self.db = next(make_session())
        super().__init__()
