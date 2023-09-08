from abc import ABC
from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session


class IRepo(ABC):

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory
