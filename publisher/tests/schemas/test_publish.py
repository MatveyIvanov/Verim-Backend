from utils.test import SchemaTestMixin


class TestSomeSchema(SchemaTestMixin):
    # TODO заглушка пока нет тестов, чтобы CI проходил
    schema_class = None

    def test_some_thing(self):
        pass
