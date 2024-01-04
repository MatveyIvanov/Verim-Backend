from schemas import (
    ChangePasswordSchema,
    ResetPasswordSchema,
    ResetPasswordConfirmSchema,
)
from utils.test import SchemaTestMixin


class TestChangePasswordSchema(SchemaTestMixin):
    schema_class = ChangePasswordSchema

    def test_current_password(self):
        self.assertNotValid(
            {"new_password": "new_password", "re_new_password": "re_new_password"}
        )
        self.assertNotValid(
            {
                "current_password": None,
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "current_password": "",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )

    def test_new_password(self):
        self.assertNotValid(
            {
                "current_password": "current_password",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "current_password": "current_password",
                "new_password": None,
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "current_password": "current_password",
                "new_password": "",
                "re_new_password": "re_new_password",
            }
        )

    def test_re_new_password(self):
        self.assertNotValid(
            {
                "current_password": "current_password",
                "new_password": "new_password",
            }
        )
        self.assertNotValid(
            {
                "current_password": "current_password",
                "new_password": "new_password",
                "re_new_password": None,
            }
        )
        self.assertNotValid(
            {
                "current_password": "current_password",
                "new_password": "new_password",
                "re_new_password": "",
            }
        )

    def test_valid(self):
        self.assertValid(
            {
                "current_password": "current_password",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )


class TestResetPasswordSchema(SchemaTestMixin):
    schema_class = ResetPasswordSchema

    def test_email(self):
        self.assertNotValid({})
        self.assertNotValid({"email": None})
        self.assertNotValid({"email": ""})
        self.assertNotValid({"email": "email"})

    def test_valid(self):
        self.assertValid({"email": "email@email.com"})


class TestResetPasswordConfirmSchema(SchemaTestMixin):
    schema_class = ResetPasswordConfirmSchema

    def test_email(self):
        self.assertNotValid(
            {
                "code": "code",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "email": None,
                "code": "code",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "email": "",
                "code": "code",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "email": "email",
                "code": "code",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )

    def test_code(self):
        self.assertNotValid(
            {
                "email": "email@email.com",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": None,
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )

    def test_new_password(self):
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "code",
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "code",
                "new_password": None,
                "re_new_password": "re_new_password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "code",
                "new_password": "",
                "re_new_password": "re_new_password",
            }
        )

    def test_re_new_password(self):
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "code",
                "new_password": "new_password",
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "code",
                "new_password": "new_password",
                "re_new_password": None,
            }
        )
        self.assertNotValid(
            {
                "email": "email@email.com",
                "code": "code",
                "new_password": "new_password",
                "re_new_password": "",
            }
        )

    def test_valie(self):
        self.assertValid(
            {
                "email": "email@email.com",
                "code": "code",
                "new_password": "new_password",
                "re_new_password": "re_new_password",
            }
        )
