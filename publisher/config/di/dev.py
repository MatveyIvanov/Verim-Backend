import re

from dependency_injector import containers, providers

import auth_pb2_grpc
from config import settings
from config.db import Database
from config.grpc import GRPCConnection

from services.validators import RegexValidator


YOUTUBE_REGEX = re.compile(
    r"/http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?[\w\?=]*)?"
)
TIKTOK_REGEX = re.compile(
    r"^.*https:\/\/(?:m|www|vm)?\.?tiktok\.com\/((?:.*\b(?:(?:usr|v|embed|user|video)\/|\?shareId=|\&item_id=)(\d+))|\w+)"
)
VK_REGEX = re.compile(r"/http(?:s?):\/\/(?:www\.)?vk.com/video.*")
TWITCH_REGEX = re.compile(r"/(?:https:\/\/)?clips\.twitch\.tv\/(\S+)/i")


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

    youtube_validator = providers.Singleton(RegexValidator, pattern=YOUTUBE_REGEX)
    tiktok_validator = providers.Singleton(RegexValidator, pattern=TIKTOK_REGEX)
    vk_validator = providers.Singleton(RegexValidator, pattern=VK_REGEX)
    twitch_validator = providers.Singleton(RegexValidator, pattern=TWITCH_REGEX)
