import os
import sqlite3
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def test_db_connection():
    """Creates a temporary sqlite3 test database."""
    _, filename = tempfile.mkstemp()
    connection = sqlite3.connect(filename)
    yield connection
    connection.close()
    os.unlink(filename)


@pytest.fixture
def test_data(test_db_connection):
    """Loads test data into the test database."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    for table in ("property", "status", "status_history"):
        with open(fixtures_dir / f"{table}.sql") as fh:
            sql = fh.read()
        cursor = test_db_connection.cursor()
        cursor.executescript(sql)
        cursor.close()
