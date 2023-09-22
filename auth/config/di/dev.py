from dependency_injector import containers, providers

from config import settings
from config.db import Database
from config.mail import SendEmail, _SendEmail
from repo import UserRepo, CodeRepo
from services.registration import RegisterUser
from services.validators import (
    Validate,
    UsernameLengthValidator,
    UsernameCharactersValidator,
    PasswordCharactersValidator,
    PasswordLengthValidator,
    PasswordRequiredCharactersValidator,
)
from services.validators.password import get_password_required_groups
from services.password import HashPassword, CheckPassword, ChangePassword
from services.jwt import CreateJWTTokens, RefreshJWTTokens, RevokeJWTTokens
from services.login import LoginUser
from services.codes import CheckCode, CreateCode, SendCode


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["endpoints"], modules=["utils.middleware", "config.celery"]
    )

    db = providers.Singleton(Database, db_url=settings.DATABASE_URL)

    _send_email = providers.Singleton(_SendEmail)
    send_email = providers.Singleton(SendEmail)

    user_repo = providers.Factory(UserRepo, session_factory=db.provided.session)
    _code_repo = providers.Factory(CodeRepo, session_factory=db.provided.session)

    create_jwt_tokens = providers.Singleton(CreateJWTTokens)
    refresh_jwt_tokens = providers.Singleton(
        RefreshJWTTokens, create_jwt_tokens=create_jwt_tokens
    )
    revoke_jwt_tokens = providers.Singleton(RevokeJWTTokens, repo=user_repo)

    username_length_validator = providers.Singleton(
        UsernameLengthValidator,
        min_length=settings.USERNAME_MIN_LENGTH,
        max_length=settings.USERNAME_MAX_LENGTH,
    )
    username_characters_validator = providers.Singleton(
        UsernameCharactersValidator,
        valid_characters=settings.USERNAME_ALLOWED_CHARACTERS,
    )
    validate_username = providers.Singleton(
        Validate,
        username_length_validator,
        username_characters_validator,
    )

    password_length_validator = providers.Singleton(
        PasswordLengthValidator,
        min_length=settings.PASSWORD_MIN_LENGTH,
        max_length=settings.PASSWORD_MAX_LENGTH,
    )
    password_characters_validator = providers.Singleton(
        PasswordCharactersValidator,
        valid_characters=settings.PASSWORD_ALLOWED_CHARACTERS,
    )
    password_required_characters_validator = providers.Singleton(
        PasswordRequiredCharactersValidator, *get_password_required_groups()
    )
    validate_password = providers.Singleton(
        Validate,
        password_length_validator,
        password_characters_validator,
        password_required_characters_validator,
    )

    hash_password = providers.Singleton(HashPassword)
    check_password = providers.Singleton(CheckPassword)

    send_code = providers.Singleton(SendCode, send_email=send_email)
    create_code = providers.Singleton(CreateCode, send_code=send_code, repo=_code_repo)
    check_code = providers.Singleton(CheckCode, repo=_code_repo)

    register_user = providers.Singleton(
        RegisterUser,
        create_code=create_code,
        validate_username=validate_username,
        validate_password=validate_password,
        hash_password=hash_password,
        repo=user_repo,
    )

    login_user = providers.Singleton(
        LoginUser,
        create_jwt_tokens=create_jwt_tokens,
        check_password=check_password,
        repo=user_repo,
    )

    change_password = providers.Singleton(
        ChangePassword,
        check_password=check_password,
        hash_password=hash_password,
        validate_password=validate_password,
        revoke_jwt_tokens=revoke_jwt_tokens,
        repo=user_repo,
    )
