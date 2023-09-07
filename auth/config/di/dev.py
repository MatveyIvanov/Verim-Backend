from dependency_injector import containers, providers

from repo import UserRepo
from services.regisration import RegisterUser
from services.validators import UsernameValidator, PasswordValidator
from services.password import SetPassword
from services.jwt import CreateJWTTokens
from utils.repo import MakeSession


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=['endpoints'])

    _make_session = providers.Singleton(MakeSession)
    _user_repo = providers.Singleton(
        UserRepo,
        make_session=_make_session
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
