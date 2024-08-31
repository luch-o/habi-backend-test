from sqlite3 import Connection

from database import Database
from models import Property, Status
from pytest_mock import MockerFixture


class TestProperty:

    def test_property_search_default(
        self, test_db_connection: Connection, test_data: None, mocker: MockerFixture
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

    def test_property_search_all_filters(
        self, test_db_connection: Connection, test_data: None, mocker: MockerFixture
    ):
        """
        GIVEN a database with a set of known records
        WHEN searching properties using all filters
        THEN the expected single instance of Property
        """
        mocker.patch.object(Database, "connect", lambda: test_db_connection)
        mocker.patch("models.SQL_PLACEHOLDER", "?")
        properties = Property.search(year=2000, city="bogota", status=Status.pre_sale)

        for property in properties:
            assert isinstance(property, Property)

        assert len(properties) == 1
