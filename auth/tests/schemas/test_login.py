from schemas import LoginSchema
from utils.test import SchemaTestMixin


class TestLoginSchema(SchemaTestMixin):
    schema_class = LoginSchema

    def test_login(self):
        self.assertNotValid({"password": "password"})
        self.assertNotValid({"login": None, "password": "password"})
        self.assertNotValid({"login": "", "password": "password"})

    def test_password(self):
        self.assertNotValid({"login": "login"})
        self.assertNotValid({"login": "login", "password": None})
        self.assertNotValid({"login": "login", "password": ""})

    def test_valid(self):
        self.assertValid({"login": "login", "password": "password"})
        self.assertValid({"login": "login@email.com", "password": "password"})
