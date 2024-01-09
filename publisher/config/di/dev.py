import re

from dependency_injector import containers, providers

import auth_pb2_grpc
from config import settings
from config.db import Database
from config.grpc import GRPCConnection

from services.validators import RegexValidator, Validate
from services.publications import CreatePublication
from repo import PublicationRepo


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

    publication_repo = providers.Singleton(
        PublicationRepo, session_factory=db.provided.session
    )

    create_publication = providers.Singleton(CreatePublication, repo=publication_repo)
