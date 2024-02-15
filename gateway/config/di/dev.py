from dependency_injector import containers, providers

import auth_pb2_grpc
import publisher_pb2_grpc
from auth_grpc_typed import AuthStub
from publisher_grpc_typed import PublisherStub
from config import settings
from config.mail import SendEmail, _SendEmail
from config.grpc import GRPCConnection


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=["endpoints"], modules=["config.celery"]
    )

    _auth_grpc = providers.Singleton(
        GRPCConnection,
        host=settings.AUTH_GRPC_HOST,
        port=settings.AUTH_GRPC_PORT,
        stub=auth_pb2_grpc.AuthStub,
    )
    _publisher_grpc = providers.Singleton(
        GRPCConnection,
        host=settings.PUBLISHER_GRPC_HOST,
        port=settings.PUBLISHER_GRPC_PORT,
        stub=publisher_pb2_grpc.PublisherStub,
    )
    auth_grpc = providers.Singleton(AuthStub, connection=_auth_grpc)
    publisher_grpc = providers.Singleton(PublisherStub, connection=_publisher_grpc)

    _send_email = providers.Singleton(_SendEmail)
    send_email = providers.Singleton(SendEmail)
