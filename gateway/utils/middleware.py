from typing import Dict

from starlette.types import Scope, Receive, Send
from fastapi import status
from fastapi.responses import JSONResponse

from config.i18n import _


def headers_from_scope(scope: Scope) -> Dict:
    return dict((k.decode().lower(), v.decode()) for k, v in scope["headers"])


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

        from auth_grpc_typed import IAuthStub, AuthRequest
        from config import settings
        from config.di import Container
        from config.i18n import _

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
            response = await Container.auth_grpc().auth(
                request=AuthRequest(token=token)
            )
            if response.user.id == -1:
                if self.raise_exception:
                    response = JSONResponse(
                        {"detail": response.error_message}, status.HTTP_401_UNAUTHORIZED
                    )
                    await response(scope, receive, send)
                else:
                    await self._app(scope, receive, send)
                return
            scope["user"] = response.user.id
        except Exception as e:  # TODO: logging
            print(str(e))
            response = JSONResponse(
                {"detail": _("Token is not correct.")}, status.HTTP_401_UNAUTHORIZED
            )
            await response(scope, receive, send)
            return

        await self._app(scope, receive, send)

    def _get_authorization_header(self, headers: Dict) -> str | None:
        try:
            from config import settings

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
        from config.i18n import activate_translation

        activate_translation(headers.get("accept-language", None))
