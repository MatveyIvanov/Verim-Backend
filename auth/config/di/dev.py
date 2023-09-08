from dependency_injector import containers, providers

from config.settings import DATABASE_URL
from config.db import Database
from repo import UserRepo
from services.regisration import RegisterUser
from services.validators import UsernameValidator, PasswordValidator
from services.password import SetPassword
from services.jwt import CreateJWTTokens


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=['endpoints'])

    db = providers.Singleton(
        Database,
        db_url=DATABASE_URL
    )

    _user_repo = providers.Factory(
        UserRepo,
        session_factory=db.provided.session
    )

    create_jwt_tokens = providers.Singleton(CreateJWTTokens)

    username_validator = providers.Singleton(UsernameValidator)
    password_validator = providers.Singleton(PasswordValidator)
    set_password = providers.Singleton(
        SetPassword,
        repo=_user_repo
    )

    register_user = providers.Singleton(
        RegisterUser,
        create_jwt_tokens=create_jwt_tokens,
        username_validator=username_validator,
        password_validator=password_validator,
        set_password=set_password,
        repo=_user_repo
    )
