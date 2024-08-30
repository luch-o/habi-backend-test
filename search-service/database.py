"""This module creates a database connection that is reused across the service."""

import os

from pymysql import Connection, connect


class Database:
    _connection: Connection | None = None

    @classmethod
    def connect(cls) -> Connection:
        """Returns a connection to the database.

        The connection to the database is establshed on the first call to Database.connect()
        afterwards, the same connection is reused.
        """
        if cls._connection is None:
            cls._connection = connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                db=os.getenv("DB_DBNAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
        return cls._connection
