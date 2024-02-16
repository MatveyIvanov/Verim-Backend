import os


TIMEZONE = os.environ.get("TIMEZONE")

PASSWORD_SALT_LENGTH = int(os.environ.get("PASSWORD_SALT_LENGTH"))
PASSWORD_HASH_ITERATIONS = int(os.environ.get("PASSWORD_HASH_ITERATIONS"))

DB_USER = os.environ.get("PUBLISHER_DB_USER")
DB_PASSWORD = os.environ.get("PUBLISHER_DB_PASSWORD")
DB_NAME = os.environ.get("PUBLISHER_DB_NAME")
DB_HOST = os.environ.get("PUBLISHER_DB_HOST")
DB_PORT = os.environ.get("PUBLISHER_DB_PORT")
DATABASE_URL = os.environ.get("PUBLISHER_DATABASE_URL")

TEST_DB_USER = os.environ.get("TEST_PUBLISHER_DB_USER")
TEST_DB_PASSWORD = os.environ.get("TEST_PUBLISHER_DB_PASSWORD")
TEST_DB_NAME = os.environ.get("TEST_PUBLISHER_DB_NAME")
TEST_DB_HOST = os.environ.get("TEST_PUBLISHER_DB_HOST")
TEST_DB_PORT = os.environ.get("TEST_PUBLISHER_DB_PORT")
TEST_DATABASE_URL = os.environ.get("TEST_PUBLISHER_DATABASE_URL")

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

PUBLISHER_GRPC_SERVER_HOST = os.environ.get("PUBLISHER_GRPC_SERVER_HOST")
PUBLISHER_GRPC_SERVER_PORT = os.environ.get("PUBLISHER_GRPC_SERVER_PORT")

PAGINATION_DEFAULT_PAGE_SIZE = os.environ.get("PAGINATION_DEFAULT_PAGE_SIZE", 20)
PAGINATION_DEFAULT_PAGE = os.environ.get("PAGINATION_DEFAULT_PAGE", 1)

APP_NAME = os.environ.get("PUBLISHER_APP_NAME")
PORT = os.environ.get("PUBLISHER_PORT")
APP_VERSION = os.environ.get("APP_VERSION")
ENVIRONMENT = os.environ.get("ENVIRONMENT")
DEBUG = bool(int(os.environ.get("DEBUG", 0)))

LOGGING_MAX_BYTES = int(os.environ.get("LOGGING_MAX_BYTES"))
LOGGING_BACKUP_COUNT = int(os.environ.get("LOGGING_BACKUP_COUNT"))
LOGGING_LOGGERS = os.environ.get("LOGGING_PUBLISHER_LOGGERS").split(",")
LOGGING_SENSITIVE_FIELDS = os.environ.get("LOGGING_AUTH_SENSITIVE_FIELDS").split(",")
LOG_PATH = os.environ.get("LOGGING_PUBLISHER_PATH")
