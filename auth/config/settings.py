import os
import string


JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
ACCESS_SECRET_KEY = os.environ.get("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY = os.environ.get("REFRESH_SECRET_KEY")
ACCESS_TOKEN_LIFETIME = int(os.environ.get("ACCESS_TOKEN_LIFETIME"))  # in minutes
REFRESH_TOKEN_LIFETIME = int(os.environ.get("REFRESH_TOKEN_LIFETIME"))  # in minutes

TIMEZONE = os.environ.get("TIMEZONE")

PASSWORD_SALT_LENGTH = int(os.environ.get("PASSWORD_SALT_LENGTH"))
PASSWORD_HASH_ITERATIONS = int(os.environ.get("PASSWORD_HASH_ITERATIONS"))

DB_USER = os.environ.get("AUTH_DB_USER")
DB_PASSWORD = os.environ.get("AUTH_DB_PASSWORD")
DB_NAME = os.environ.get("AUTH_DB_NAME")
DB_HOST = os.environ.get("AUTH_DB_HOST")
DB_PORT = os.environ.get("AUTH_DB_PORT")
DATABASE_URL = os.environ.get("AUTH_DATABASE_URL")

USERNAME_MIN_LENGTH = int(os.environ.get("USERNAME_MIN_LENGTH"))
USERNAME_MAX_LENGTH = int(os.environ.get("USERNAME_MAX_LENGTH"))
USERNAME_ALLOWED_SPECIAL_CHARACTERS = os.environ.get(
    "USERNAME_ALLOWED_SPECIAL_CHARACTERS"
)
USERNAME_ALLOWED_CHARACTERS = (
    string.ascii_letters + string.digits + USERNAME_ALLOWED_SPECIAL_CHARACTERS
)

PASSWORD_MIN_LENGTH = int(os.environ.get("PASSWORD_MIN_LENGTH"))
PASSWORD_MAX_LENGTH = int(os.environ.get("PASSWORD_MAX_LENGTH"))
PASSWORD_ALLOWED_CHARACTERS = string.printable

AUTHENTICATION_HEADER = os.environ.get("AUTHENTICATION_HEADER")
AUTHENTICATION_HEADER_PREFIX = os.environ.get("AUTHENTICATION_HEADER_PREFIX")

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
MAIL_FROM = os.environ.get("MAIL_FROM")
MAIL_PORT = int(os.environ.get("MAIL_PORT"))
MAIL_SERVER = os.environ.get("MAIL_SERVER")
MAIL_FROM_NAME = os.environ.get("MAIL_FROM_NAME")

CONFIRM_EMAIL_CODE_DURATION = int(
    os.environ.get("CONFIRM_EMAIL_CODE_DURATION")
)  # seconds
CONFIRM_EMAIL_CHECK_DELAY = int(os.environ.get("CONFIRM_EMAIL_CHECK_DELAY"))  # seconds

RESET_PASSWORD_CODE_DURATION = int(
    os.environ.get("RESET_PASSWORD_CODE_DURATION")
)  # seconds

CONFIRMATION_CODE_LENGTH = int(os.environ.get("CONFIRMATION_CODE_LENGTH"))
CONFIRMATION_CODE_CHARACTERS = string.digits

AUTH_GRPC_SERVER_HOST = os.environ.get("AUTH_GRPC_SERVER_HOST")
AUTH_GRPC_SERVER_PORT = os.environ.get("AUTH_GRPC_SERVER_PORT")

PUBLISHER_GRPC_HOST = os.environ.get("PUBLISHER_GRPC_HOST")
PUBLISHER_GRPC_PORT = os.environ.get("PUBLISHER_GRPC_PORT")
