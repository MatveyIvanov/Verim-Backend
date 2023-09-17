from typing import Dict

from dependency_injector.wiring import inject, Provide
from starlette.types import Scope, Receive, Send
from fastapi import status
from fastapi.responses import JSONResponse
import jwt

from config import settings
from config.di import Container
from config.i18n import activate_translation, _
from services.repo import IUserRepo
from services.entries import JWTPayload
from utils.time import timestamp_to_datetime
from utils.typing import UserType
from utils.exceptions import Custom401Exception, Custom403Exception


def headers_from_scope(scope: Scope) -> Dict:
    return dict((k.decode().lower(), v.decode()) for k, v in scope["headers"])


@inject
def authenticate_by_token(
    token: str | bytes,
    access: bool = True,
    repo: IUserRepo = Provide[Container.user_repo],
):
    try:
        payload: Dict = jwt.decode(
            token,
            settings.ACCESS_SECRET_KEY if access else settings.REFRESH_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except jwt.exceptions.PyJWTError as e:
        raise Custom401Exception(_("Token is not correct."))

    try:
        payload: JWTPayload = JWTPayload(**payload)
    except TypeError:
        raise Custom401Exception(_("Token is not correct."))

    user: UserType = repo.get_by_id(payload.user)
    if not user:
        raise Custom401Exception(_("Token is not correct."))

    if user.tokens_revoked_at and user.tokens_revoked_at > timestamp_to_datetime(
        payload.created_at
    ):
        raise Custom401Exception(_("Token is not correct."))

    if not user.is_active:
        raise Custom403Exception(_("User is not active."))

    return user


class AuthenticationMiddleware:
    def __init__(self, app, raise_exception: bool = True):
        self._app = app
        self.raise_exception = raise_exception

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if not scope["type"] == "http":
            await self._app(scope, receive, send)

        scope["user"] = None
        headers = headers_from_scope(scope)

        auth_header = self._get_authorization_header(headers)
        if auth_header is None:
            if self.raise_exception:
                response = JSONResponse(
                    {"detail": "Credentials not provided."},
                    status.HTTP_401_UNAUTHORIZED,
                )
                await response(scope, receive, send)
            else:
                await self._app(scope, receive, send)
            return

        auth_header = auth_header.split()

        if len(auth_header) != 2:
            if self.raise_exception:
                response = JSONResponse(
                    {"detail": "Authentication failed."}, status.HTTP_401_UNAUTHORIZED
                )
                await response(scope, receive, send)
            else:
                await self._app(scope, receive, send)
            return

        prefix, token = auth_header

        if prefix.lower() != settings.AUTHENTICATION_HEADER_PREFIX.lower():
            if self.raise_exception:
                response = JSONResponse(
                    {"detail": "Authentication failed."}, status.HTTP_401_UNAUTHORIZED
                )
                await response(scope, receive, send)
            else:
                await self._app(scope, receive, send)
            return

        try:
            scope["user"] = authenticate_by_token(token)
        except (Custom401Exception, Custom403Exception) as e:
            if self.raise_exception:
                response = JSONResponse({"detail": str(e)}, status.HTTP_403_FORBIDDEN)
                await response(scope, receive, send)
            else:
                await self._app(scope, receive, send)
            return

        await self._app(scope, receive, send)

    def _get_authorization_header(self, headers: Dict) -> str | None:
        try:
            return headers[settings.AUTHENTICATION_HEADER.lower()]
        except KeyError:
            return None


class TranslationMiddleware:
    def __init__(self, app):
        self._app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if not scope["type"] == "http":
            await self._app(scope, receive, send)

        headers = self._get_headers(scope)
        self._activate_translation(headers)

        await self._app(scope, receive, send)

    def _get_headers(self, scope: Scope) -> Dict:
        return headers_from_scope(scope)

    def _activate_translation(self, headers: Dict) -> None:
        activate_translation(headers.get("accept-language", None))
