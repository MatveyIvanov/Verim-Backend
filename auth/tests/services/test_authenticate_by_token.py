from unittest import mock
from datetime import datetime, timedelta

import pytest
from pytest_mock import MockerFixture
from jwt.exceptions import PyJWTError

from config import settings
from config.di import get_di_test_container
from services.login import LoginUser
from schemas import LoginSchema, JWTTokensSchema
from repo.user import UserRepo
from utils.test import ServiceTestMixin
from utils.exceptions import Custom401Exception, Custom403Exception
from utils.middleware import authenticate_by_token


container = get_di_test_container()


class TestAuthenticateByToken(ServiceTestMixin):
    def setup_method(self):
        self.now = datetime(10, 10, 10)
        self.token = "token"
        self.payload = {
            "user": self.user.id,
            "exp": self.now.timestamp(),
            "created_at": (
                self.now - timedelta(minutes=settings.ACCESS_TOKEN_LIFETIME)
            ),
        }

        self.user_repo = mock.Mock()
        self.user_repo.get_by_id.return_value = self.user

        self.context = container.user_repo.override(self.user_repo)

    def test_access_jwt_error(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.exceptions.PyJWTError = PyJWTError
        jwt.decode.side_effect = PyJWTError
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=True, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.ACCESS_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_not_called()
            timestamp_to_datetime.assert_not_called()

    def test_access_payload_error(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        self.payload.pop("created_at")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=True, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.ACCESS_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_not_called()
            timestamp_to_datetime.assert_not_called()

    def test_access_user_not_found(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")

        self.user_repo.get_by_id.return_value = None
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=True, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.ACCESS_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_not_called()

    def test_access_token_revoked(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        timestamp_to_datetime.return_value = self.now - timedelta(seconds=1)

        self.user.tokens_revoked_at = self.now
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=True, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.ACCESS_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_called_once_with(self.payload["created_at"])
        self.user.tokens_revoked_at = None

    def test_access_user_not_active(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")

        self.user.is_active = False
        with self.context, pytest.raises(Custom403Exception):
            authenticate_by_token(self.token, access=True, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.ACCESS_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_not_called()
        self.user.is_active = True

    def test_refresh_jwt_error(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.exceptions.PyJWTError = PyJWTError
        jwt.decode.side_effect = PyJWTError
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=False, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_not_called()
            timestamp_to_datetime.assert_not_called()

    def test_refresh_payload_error(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        self.payload.pop("created_at")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=False, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_not_called()
            timestamp_to_datetime.assert_not_called()

    def test_refresh_user_not_found(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")

        self.user_repo.get_by_id.return_value = None
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=False, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_not_called()

    def test_refresh_token_revoked(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        timestamp_to_datetime.return_value = self.now - timedelta(seconds=1)

        self.user.tokens_revoked_at = self.now
        with self.context, pytest.raises(Custom401Exception):
            authenticate_by_token(self.token, access=False, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_called_once_with(self.payload["created_at"])
        self.user.tokens_revoked_at = None

    def test_refresh_user_not_active(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")

        self.user.is_active = False
        with self.context, pytest.raises(Custom403Exception):
            authenticate_by_token(self.token, access=False, repo=self.user_repo)

            jwt.decode.assert_called_once_with(
                self.token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_not_called()
        self.user.is_active = True

    def test_authenticate_by_access(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        with self.context:
            user = authenticate_by_token(self.token, access=True, repo=self.user_repo)

            assert user == self.user
            jwt.decode.assert_called_once_with(
                self.token,
                settings.ACCESS_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_not_called()

    def test_authenticate_by_refresh(self, mocker: MockerFixture):
        jwt = mocker.patch("utils.middleware.jwt")
        jwt.decode.return_value = self.payload
        timestamp_to_datetime = mocker.patch("utils.middleware.timestamp_to_datetime")
        with self.context:
            user = authenticate_by_token(self.token, access=False, repo=self.user_repo)

            assert user == self.user
            jwt.decode.assert_called_once_with(
                self.token,
                settings.REFRESH_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM],
            )
            self.user_repo.get_by_id.assert_called_once_with(self.payload["user"])
            timestamp_to_datetime.assert_not_called()
