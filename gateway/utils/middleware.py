import math
import time
import json
import logging
import http
from typing import Dict

from starlette.types import Scope, Receive, Send
from fastapi import status, Request, Response
from fastapi.responses import JSONResponse

from config.settings import PORT
from config.i18n import _
from utils.logging import RequestJsonLogSchema, EMPTY_VALUE


requests_logger = logging.getLogger("requests")
auth_logger = logging.getLogger("auth")


def headers_from_scope(scope: Scope) -> Dict:
    return dict((k.decode().lower(), v.decode()) for k, v in scope["headers"])


class AuthenticationMiddleware:
    def __init__(self, app, raise_exception: bool = True):
        self._app = app
        self.raise_exception = raise_exception

    async def __call__(self, scope: Scope, receive: Receive, send: Send):  # noqa: C901
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

        from auth_grpc_typed import AuthRequest
        from config import settings
        from config.di import Container

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
        except Exception as e:
            requests_logger.error(
                f"Error while authenticating user - {str(e)}",
                exc_info=e,
            )
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


class LoggingMiddleware:
    """
    Middleware для обработки запросов и ответов
    с целью журналирования (https://habr.com/ru/articles/575454/)
    """

    @staticmethod
    async def get_protocol(request: Request) -> str:
        protocol = str(request.scope.get("type", ""))
        http_version = str(request.scope.get("http_version", ""))
        if protocol.lower() == "http" and http_version:
            return f"{protocol.upper()}/{http_version}"
        return EMPTY_VALUE

    @staticmethod
    async def set_body(request: Request, body: bytes) -> None:
        async def receive():
            return {"type": "http.request", "body": body}

        request._receive = receive

    async def get_body(self, request: Request) -> Dict:
        body = await request.body()
        await self.set_body(request, body)
        return await request.json()

    async def __call__(self, request: Request, call_next, *args, **kwargs):
        if "docs" in str(request.url):
            return await call_next(request)
        start_time = time.time()
        exception_object = None
        # Request Side
        try:
            raw_request_body = await request.body()
            # Последующие действия нужны,
            # чтобы не перезатереть тело запроса
            # и не уйти в зависание event-loop'a
            # при последующем получении тела ответа
            await self.set_body(request, raw_request_body)
            request_body = await self.get_body(request)
        except Exception:
            request_body = EMPTY_VALUE

        server: tuple = request.get("server", ("localhost", PORT))
        request_headers: dict = dict(request.headers.items())
        # Response Side
        try:
            response = await call_next(request)
        except Exception as ex:
            response_body = bytes(http.HTTPStatus.INTERNAL_SERVER_ERROR.phrase.encode())
            response = Response(
                content=response_body,
                status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR.real,
            )
            exception_object = ex
            response_headers = {}
        else:
            response_headers = dict(response.headers.items())
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            response = Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
        duration: int = math.ceil((time.time() - start_time) * 1000)
        response_body = response_body.decode()
        # Инициализация и формирования полей для запроса-ответа
        request_json_fields = RequestJsonLogSchema(
            request_uri=str(request.url),
            request_referer=request_headers.get("referer", EMPTY_VALUE),
            request_protocol=await self.get_protocol(request),
            request_method=request.method,
            request_path=request.url.path,
            request_host=f"{server[0]}:{server[1]}",
            request_size=int(request_headers.get("content-length", 0)),
            request_content_type=request_headers.get("content-type", EMPTY_VALUE),
            request_headers=request_headers,
            request_body=request_body or {},
            request_direction="in",
            remote_ip=request.client[0],
            remote_port=request.client[1],
            response_status_code=response.status_code,
            response_size=int(response_headers.get("content-length", 0)),
            response_headers=response_headers,
            response_body=json.loads(response_body) if response_body else {},
            duration=duration,
        ).dict()
        # Хочется на каждый запрос читать
        # и понимать в сообщении самое главное,
        # поэтому message мы сразу делаем типовым
        message = (
            f'{"Ошибка" if exception_object else "Ответ"} '
            f"с кодом {response.status_code} "
            f'на запрос {request.method} "{str(request.url)}", '
            f"за {duration} мс"
        )
        getattr(requests_logger, "error" if exception_object else "info")(
            message,
            extra={
                "request_json_fields": request_json_fields,
                "to_mask": True,
            },
            exc_info=exception_object,
        )
        return response
