from database import Database
from models import Property
from pytest_mock import MockerFixture


class TestProperty:

    def test_property_search_default(
        self, test_db_connection, test_data, mocker: MockerFixture
    ):
        """
        GIVEN a database with a set of known records.
        WHEN searching properties
        THEN a known number of Property instances are returned
        """
        mocker.patch.object(Database, "connect", lambda: test_db_connection)
        properties = Property.search()

        for property in properties:
            assert isinstance(property, Property)

        assert len(properties) == 6
