from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict

from config.grpc import GRPCConnection
from utils.exceptions import Custom400Exception


def handle_error(func):
    async def wrapper(*args, **kwargs):
        response = await func(*args, **kwargs)
        if getattr(response, "detail", None):
            raise Custom400Exception(detail=response.detail)
        return response

    return wrapper


@dataclass
class Empty:
    detail: str | None


@dataclass
class AuthRequest:
    token: str


@dataclass
class User:
    id: int


@dataclass
class AuthResponse:
    user: User


@dataclass
class LoginRequest:
    login: str
    password: str


@dataclass
class JWTTokens:
    access: str
    refresh: str
    detail: str | None


@dataclass
class CodeSentResponse:
    email: str
    message: str
    detail: str | None


@dataclass
class RefreshTokensRequest:
    refresh: str


@dataclass
class ChangePasswordRequest:
    user_id: int
    current_password: int
    new_password: int
    re_new_password: int


@dataclass
class ResetPasswordRequest:
    email: str


@dataclass
class ResetPasswordConfirmRequest:
    email: str
    code: str
    new_password: str
    re_new_password: str


@dataclass
class RegisterRequest:
    email: str
    username: str
    password: str
    re_password: str


@dataclass
class RepeatRegisterRequest:
    email: str


@dataclass
class ConfirmRegisterRequest:
    email: str
    code: str


class IAuthStub(ABC):
    @abstractmethod
    async def auth(self, request: AuthRequest) -> AuthResponse: ...

    @abstractmethod
    def jwt_refresh(self, request: RefreshTokensRequest) -> JWTTokens: ...

    @abstractmethod
    async def login(self, request: LoginRequest) -> JWTTokens: ...

    @abstractmethod
    def password_change(self, request: ChangePasswordRequest) -> Empty: ...

    @abstractmethod
    def password_reset(self, request: ResetPasswordRequest) -> CodeSentResponse: ...

    @abstractmethod
    def password_reset_confirm(self, request: ResetPasswordConfirmRequest) -> Empty: ...

    @abstractmethod
    def register(self, request: RegisterRequest) -> CodeSentResponse: ...

    @abstractmethod
    def register_repeat(self, request: RepeatRegisterRequest) -> CodeSentResponse: ...

    @abstractmethod
    def register_confirm(self, request: ConfirmRegisterRequest) -> JWTTokens: ...


class AuthStub(IAuthStub):
    def __init__(self, connection: GRPCConnection) -> None:
        self.connection = connection

    @handle_error
    async def auth(self, request: AuthRequest) -> AuthResponse:
        from auth_pb2 import AuthRequest as _AuthRequest

        response = await self.connection.stub.auth(_AuthRequest(**asdict(request)))
        return AuthResponse(user=User(id=response.user.id))

    @handle_error
    async def jwt_refresh(self, request: RefreshTokensRequest) -> JWTTokens:
        from auth_pb2 import RefreshTokensRequest as _RefreshTokensRequest

        response = await self.connection.stub.jwt_refresh(
            _RefreshTokensRequest(**asdict(request))
        )
        return JWTTokens(
            access=response.access,
            refresh=response.refresh,
            detail=response.detail,
        )

    @handle_error
    async def login(self, request: LoginRequest) -> JWTTokens:
        from auth_pb2 import LoginRequest as _LoginRequest

        response = await self.connection.stub.login(_LoginRequest(**asdict(request)))
        return JWTTokens(
            access=response.access,
            refresh=response.refresh,
            detail=response.detail,
        )

    @handle_error
    async def password_change(self, request: ChangePasswordRequest) -> Empty:
        from auth_pb2 import ChangePasswordRequest as _ChangePasswordRequest

        response = await self.connection.stub.password_change(
            _ChangePasswordRequest(**asdict(request))
        )
        return Empty(detail=response.detail)

    @handle_error
    async def password_reset(self, request: ResetPasswordRequest) -> CodeSentResponse:
        from auth_pb2 import ResetPasswordRequest as _ResetPasswordRequest

        response = await self.connection.stub.password_reset(
            _ResetPasswordRequest(**asdict(request))
        )
        return CodeSentResponse(
            email=response.email,
            message=response.message,
            detail=response.detail,
        )

    @handle_error
    async def password_reset_confirm(
        self, request: ResetPasswordConfirmRequest
    ) -> Empty:
        from auth_pb2 import ResetPasswordConfirmRequest as _ResetPasswordConfirmRequest

        response = await self.connection.stub.password_reset_confirm(
            _ResetPasswordConfirmRequest(**asdict(request))
        )
        return Empty(detail=response.detail)

    @handle_error
    async def register(self, request: RegisterRequest) -> CodeSentResponse:
        from auth_pb2 import RegisterRequest as _RegisterRequest

        response = await self.connection.stub.register(
            _RegisterRequest(**asdict(request))
        )
        return CodeSentResponse(
            email=response.email,
            message=response.message,
            detail=response.detail,
        )

    @handle_error
    async def register_repeat(self, request: RepeatRegisterRequest) -> CodeSentResponse:
        from auth_pb2 import RepeatRegisterRequest as _RepeatRegisterRequest

        response = await self.connection.stub.register_repeat(
            _RepeatRegisterRequest(**asdict(request))
        )
        return CodeSentResponse(
            email=response.email,
            message=response.message,
            detail=response.detail,
        )

    @handle_error
    async def register_confirm(self, request: ConfirmRegisterRequest) -> JWTTokens:
        from auth_pb2 import ConfirmRegisterRequest as _ConfirmRegisterRequest

        response = await self.connection.stub.register_confirm(
            _ConfirmRegisterRequest(**asdict(request))
        )
        return JWTTokens(
            access=response.access,
            refresh=response.refresh,
            detail=response.detail,
        )