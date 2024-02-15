from schemas.auth import RefreshTokensSchema
from utils.test import SchemaTestMixin


class TestRefreshTokensSchema(SchemaTestMixin):
    schema_class = RefreshTokensSchema

    def test_refresh(self):
        self.assertNotValid({})
        self.assertNotValid({"refresh": None})
        self.assertNotValid({"refresh": ""})
        self.assertValid({"refresh": "refresh"})
