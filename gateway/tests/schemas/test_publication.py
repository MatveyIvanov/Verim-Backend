from schemas.publisher import CreatePublicationSchema
from utils.test import SchemaTestMixin


class TestCreatePublicationSchema(SchemaTestMixin):
    schema_class = CreatePublicationSchema

    def test_url(self):
        self.assertNotValid({})
        self.assertNotValid({"url": None})
        self.assertNotValid({"url": ""})
        self.assertNotValid({"url": "url"})
        self.assertValid({"url": "https://example.com"})
