from typing import Any, Dict

from fastapi.exceptions import HTTPException
from fastapi import status


class CustomException(HTTPException):
    pass


class Custom400Exception(CustomException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class Custom401Exception(CustomException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)


class Custom403Exception(CustomException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)


class Custom404Exception(CustomException):
    def __init__(
        self, detail: Any = None, headers: Dict[str, str] | None = None
    ) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)
