import os


TIMEZONE = "Europe/Moscow"

PASSWORD_SALT_LENGTH = 20
PASSWORD_HASH_ITERATIONS = 100_100

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DATABASE_URL = os.environ.get("DATABASE_URL")

AUTHENTICATION_HEADER = "Authorization"  # TODO: В env
AUTHENTICATION_HEADER_PREFIX = "Bearer"  # TODO: В env

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PORT = int(os.environ.get("MAIL_PORT"))
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME")

AUTH_GRPC_HOST = os.environ.get("AUTH_GRPC_HOST")
AUTH_GRPC_PORT = os.environ.get("AUTH_GRPC_PORT")
