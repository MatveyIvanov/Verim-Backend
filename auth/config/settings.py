import os


ACCESS_SECRET_KEY = os.environ.get('ACCESS_SECRET_KEY', 'ACCESS_SECRET_KEY')  # FIXME
REFRESH_SECRET_KEY = os.environ.get('REFRESH_SECRET_KEY', 'REFRESH_SECRET_KEY')  # FIXME
ACCESS_TOKEN_LIFETIME = 8 * 60  # in minutes
REFRESH_TOKEN_LIFETIME = 48 * 60  # in minutes

TIMEZONE = 'Europe/Moscow'

PASSWORD_SALT_LENGTH = 20
PASSWORD_HASH_ITERATIONS = 100_100

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DATABASE_URL = os.environ.get('DATABASE_URL')
