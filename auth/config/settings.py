import os
import string


JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")  # FIXME
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY", "ACCESS_SECRET_KEY")  # FIXME
REFRESH_SECRET_KEY = os.environ.get("REFRESH_SECRET_KEY", "REFRESH_SECRET_KEY")  # FIXME
ACCESS_TOKEN_LIFETIME = 8 * 60  # in minutes
REFRESH_TOKEN_LIFETIME = 48 * 60  # in minutes

TIMEZONE = "Europe/Moscow"

PASSWORD_SALT_LENGTH = 20
PASSWORD_HASH_ITERATIONS = 100_100

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DATABASE_URL = os.environ.get("DATABASE_URL")

USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 20
USERNAME_ALLOWER_SPECIAL_CHARACTERS = ".-_"
USERNAME_ALLOWED_CHARACTERS = (
    string.ascii_letters + string.digits + USERNAME_ALLOWER_SPECIAL_CHARACTERS
)

PASSWORD_MIN_LENGTH = 8
PASSWORD_MAX_LENGTH = 30
PASSWORD_ALLOWED_CHARACTERS = string.printable

AUTHENTICATION_HEADER = "Authorization"  # TODO: В env
AUTHENTICATION_HEADER_PREFIX = "Bearer"  # TODO: В env

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PORT = int(os.environ.get("MAIL_PORT"))
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME")

CONFIRM_EMAIL_CODE_DURATION = 60  # seconds
CONFIRM_EMAIL_CHECK_DELAY = 600  # seconds

RESET_PASSWORD_CODE_DURATION = 60  # seconds

AUTH_GRPC_SERVER_HOST = os.environ.get("AUTH_GRPC_SERVER_HOST")
AUTH_GRPC_SERVER_PORT = os.environ.get("AUTH_GRPC_SERVER_PORT")
