from dependency_injector.wiring import inject, Provide
from starlette.types import Scope, Receive, Send
from fastapi import status
from fastapi.responses import JSONResponse
import jwt

from config import settings
from config.di import Container
from services.repo import IUserRepo
from utils.exceptions import Custom401Exception, Custom403Exception
from utils.time import get_current_time


@inject
def authenticate_by_token(token, repo: IUserRepo = Provide[Container.user_repo]):
    try:
        payload = jwt.decode(
            token, settings.ACCESS_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
    except jwt.exceptions.PyJWTError:
        raise Custom401Exception("Token is not correct.")

    user = repo.get_by_id(payload.get("user", None))
    if not user:
        raise Custom401Exception("Token is not correct.")
    # TODO: check for last tokens revokation time

    if not user.is_active:
        raise Custom403Exception("User is not active.")

    return user


class AuthenticationMiddleware:
    def __init__(self, app, raise_exception: bool = True):
        self._app = app
        self.raise_exception = raise_exception

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if not scope["type"] == "http":
            await self._app(scope, receive, send)

        scope["user"] = None

        auth_header = self._get_authorization_header(scope).split()
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

    def _get_authorization_header(self, scope: Scope) -> str | None:
        headers = dict((k.decode().lower(), v.decode()) for k, v in scope["headers"])
        try:
            return headers[settings.AUTHENTICATION_HEADER.lower()]
        except KeyError:
            return None
