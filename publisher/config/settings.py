import os


TIMEZONE = "Europe/Moscow"

PASSWORD_SALT_LENGTH = int(os.environ.get("PASSWORD_SALT_LENGTH"))
PASSWORD_HASH_ITERATIONS = int(os.environ.get("PASSWORD_HASH_ITERATIONS"))

DB_USER = os.environ.get("PUBLISHER_DB_USER")
DB_PASSWORD = os.environ.get("PUBLISHER_DB_PASSWORD")
DB_NAME = os.environ.get("PUBLISHER_DB_NAME")
DB_HOST = os.environ.get("PUBLISHER_DB_HOST")
DB_PORT = os.environ.get("PUBLISHER_DB_PORT")
DATABASE_URL = os.environ.get("PUBLISHER_DATABASE_URL")

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
