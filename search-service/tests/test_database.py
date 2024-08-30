from sqlite3 import Connection

from database import Database
from pytest_mock import MockerFixture


class TestDatabase:

    def test_connection_is_reused(
        self, test_db_connection: Connection, mocker: MockerFixture
    ):
        """
        GIVEN a database
        WHEN requesting a connection from the classmethod more than once
        THEN the same connection is reused
        """
        # mock connect imported from mysql and replace with connection to test sqlite db
        mocker.patch("database.connect", return_value=test_db_connection)
        conn1 = Database.connect()
        conn2 = Database.connect()

        assert conn1 is conn2

    def test_connection_is_reused_from_instances(
        self, test_db_connection: Connection, mocker: MockerFixture
    ):
        """
        GIVEN a database
        WHEN requesting a connection from instnces of the Database class more than once
        THEN the same connection is reused
        """
        # mock connect imported from mysql and replace with connection to test sqlite db
        mocker.patch("database.connect", return_value=test_db_connection)
        conn1 = Database().connect()
        conn2 = Database().connect()

        assert conn1 is conn2
