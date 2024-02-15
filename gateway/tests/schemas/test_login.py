from schemas.auth import LoginSchema
from utils.test import SchemaTestMixin


class TestLoginSchema(SchemaTestMixin):
    schema_class = LoginSchema

    def test_login(self):
        self.assertNotValid({"password": "password"})
        self.assertNotValid({"login": None, "password": "password"})
        self.assertNotValid({"login": "", "password": "password"})
        self.assertValid({"login": "username", "password": "password"})
        self.assertValid({"login": "email@email.com", "password": "password"})

    def test_password(self):
        self.assertNotValid({"login": "username"})
        self.assertNotValid({"login": "username", "password": None})
        self.assertNotValid({"login": "username", "password": ""})
        self.assertValid({"login": "username", "password": "password"})
