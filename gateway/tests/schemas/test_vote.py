from schemas.publisher import VoteSchema
from utils.test import SchemaTestMixin


class TestVoteSchema(SchemaTestMixin):
    schema_class = VoteSchema

    def test_believed(self):
        self.assertNotValid({})
        self.assertValid({"believed": None})
        self.assertValid({"believed": True})
        self.assertValid({"believed": False})
