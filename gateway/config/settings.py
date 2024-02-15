import os


TIMEZONE = os.environ.get("TIMEZONE")

AUTHENTICATION_HEADER = os.environ.get("AUTHENTICATION_HEADER")
AUTHENTICATION_HEADER_PREFIX = os.environ.get("AUTHENTICATION_HEADER_PREFIX")

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PORT = int(os.environ.get("MAIL_PORT"))
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME")

AUTH_GRPC_HOST = os.environ.get("AUTH_GRPC_HOST")
AUTH_GRPC_PORT = os.environ.get("AUTH_GRPC_PORT")

PUBLISHER_GRPC_HOST = os.environ.get("PUBLISHER_GRPC_HOST")
PUBLISHER_GRPC_PORT = os.environ.get("PUBLISHER_GRPC_PORT")

CONFIRMATION_CODE_LENGTH = int(os.environ.get("CONFIRMATION_CODE_LENGTH"))

APP_NAME = os.environ.get("GETEWAY_APP_NAME")
PORT = os.environ.get("GATEWAY_PORT")
APP_VERSION = os.environ.get("APP_VERSION")
ENVIRONMENT = os.environ.get("ENVIRONMENT")
DEBUG = bool(int(os.environ.get("DEBUG", 0)))

LOGGING_MAX_BYTES = int(os.environ.get("LOGGING_MAX_BYTES"))
LOGGING_BACKUP_COUNT = int(os.environ.get("LOGGING_BACKUP_COUNT"))
LOGGING_LOGGERS = os.environ.get("LOGGING_GATEWAY_LOGGERS").split(",")
LOGGING_SENSITIVE_FIELDS = os.environ.get("LOGGING_GATEWAY_SENSITIVE_FIELDS").split(",")
LOG_PATH = os.environ.get("LOGGING_GATEWAY_PATH")
