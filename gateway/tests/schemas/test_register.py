from config import settings
from schemas.auth import (
    RegistrationSchema,
    ConfirmRegistrationSchema,
    RepeatRegistrationCodeSchema,
)
from utils.test import SchemaTestMixin


class TestRegistrationSchema(SchemaTestMixin):
    schema_class = RegistrationSchema

    def test_email(self):
        self.assertNotValid(
            {
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": None,
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": "",
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": "email",
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )
        self.assertValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )

    def test_username(self):
        self.assertNotValid(
            {
                "email": "email@email.com",
                "password": "password",
                "re_password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": None,
                "password": "password",
                "re_password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": "",
                "password": "password",
                "re_password": "password",
            }
        )
        self.assertValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )

    def test_password(self):
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": "username",
                "re_password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": None,
                "re_password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "",
                "re_password": "password",
            }
        )
        self.assertValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )

    def test_re_password(self):
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "password",
                "re_password": None,
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "password",
                "re_password": "",
            }
        )
        self.assertValid(
            {
                "email": "email@email.com",
                "username": "username",
                "password": "password",
                "re_password": "password",
            }
        )


class TestConfirmRegistrationSchema(SchemaTestMixin):
    schema_class = ConfirmRegistrationSchema

    def test_email(self):
        self.assertNotValid({"code": "code"})
        self.assertNotValid(
            {
                "email": None,
                "code": "code",
            }
        )
        self.assertNotValid(
            {
                "email": "",
                "code": "code",
            }
        )
        self.assertNotValid(
            {
                "email": "email",
                "code": "code",
            }
        )
        self.assertValid(
            {
                "email": "email@email.com",
                "code": "code",
            }
        )

    def test_code(self):
        self.assertNotValid(
            {
                "email": "email@email.com",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": None,
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "a" * (settings.CONFIRMATION_CODE_LENGTH - 1),
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "a" * (settings.CONFIRMATION_CODE_LENGTH + 1),
            }
        )
        self.assertValid(
            {
                "email": "email@email.com",
                "code": "code",
            }
        )


class TestRepeatRegistrationCodeSchema(SchemaTestMixin):
    schema_class = RepeatRegistrationCodeSchema

    def test_email(self):
        self.assertNotValid({})
        self.assertNotValid({"email": None})
        self.assertNotValid({"email": ""})
        self.assertNotValid({"email": "email"})
        self.assertValid({"email": "email@email.com"})
