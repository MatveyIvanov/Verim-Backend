from unittest import mock

from pytest_mock import MockerFixture

from config.di import get_di_test_container
from services.jwt import RefreshJWTTokens
from schemas import JWTTokensSchema, RefreshTokensSchema
from utils.test import ServiceTestMixin


container = get_di_test_container()


class TestRefreshJWTTokens(ServiceTestMixin):
    def setup_method(self):
        self.entry = RefreshTokensSchema(refresh="refresh")

        self.tokens = JWTTokensSchema(
            access="access",
            refresh="refresh",
        )

        self.create_jwt_tokens = mock.Mock()
        self.create_jwt_tokens.return_value = self.tokens

        self.context = container.refresh_jwt_tokens.override(
            RefreshJWTTokens(create_jwt_tokens=self.create_jwt_tokens)
        )

    def test_refresh(self, mocker: MockerFixture):
        authenticate_by_token = mocker.patch(
            "services.jwt.refresh.authenticate_by_token"
        )
        authenticate_by_token.return_value = self.user
        with self.context:
            tokens = container.refresh_jwt_tokens()(self.entry)

            assert isinstance(tokens, JWTTokensSchema)
            assert tokens == self.tokens
            authenticate_by_token.assert_called_once_with(
                self.entry.refresh, access=False
            )
            self.create_jwt_tokens.assert_called_once_with(user=self.user)
