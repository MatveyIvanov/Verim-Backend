import re

from dependency_injector import containers, providers

import auth_pb2_grpc
from config import settings
from config.db import Database
from config.grpc import GRPCConnection

from services.validators import RegexValidator, Validate
from services.publications import CreatePublication
from repo import PublicationRepo

from utils.regex import YOUTUBE_REGEX, TIKTOK_REGEX, VK_REGEX, TWITCH_REGEX


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["endpoints"], modules=["utils.middleware", "config.celery"]
    )

    auth_grpc = providers.Singleton(
        GRPCConnection,
        host=settings.AUTH_GRPC_HOST,
        port=settings.AUTH_GRPC_PORT,
        stub=auth_pb2_grpc.AuthStub,
    )

    db = providers.Singleton(Database, db_url=settings.DATABASE_URL)

    _publication_repo = providers.Singleton(
        PublicationRepo, session_factory=db.provided.session
    )

    _youtube_validator = providers.Singleton(RegexValidator, pattern=YOUTUBE_REGEX)
    _tiktok_validator = providers.Singleton(RegexValidator, pattern=TIKTOK_REGEX)
    _vk_validator = providers.Singleton(RegexValidator, pattern=VK_REGEX)
    _twitch_validator = providers.Singleton(RegexValidator, pattern=TWITCH_REGEX)
    _validate_platform = providers.Singleton(
        Validate,
        _youtube_validator,
        _tiktok_validator,
        _vk_validator,
        _twitch_validator,
    )

    create_publication = providers.Singleton(
        CreatePublication, repo=_publication_repo, validate_url=_validate_platform
    )
