"""Test the service with sanmple events."""

import json
from pathlib import Path
from sqlite3 import Connection

import pytest
from database import Database
from handler import handler
from httputil import StatusCodes
from pytest_mock import MockerFixture


def load_json_event(filename: str):
    """Utility to load json fixtures."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    with open(fixtures_dir / f"{filename}.json") as f:
        event = json.load(f)
    return event


class TestHandler:

    @pytest.fixture
    def search_all_event(self) -> dict:
        """Valid event to search all properties."""
        return load_json_event("event_valid")

    @pytest.fixture
    def search_with_filters_event(self) -> dict:
        """Valid event to search properties with filters."""
        return load_json_event("event_with_filters")

    @pytest.fixture
    def search_invalid_method_event(self) -> dict:
        """Event with an unsupported HTTP method."""
        return load_json_event("event_invalid_method")

    @pytest.fixture
    def search_invalid_status_event(self) -> dict:
        """Event with an unsupported status as fitlter."""
        return load_json_event("event_invalid_status")

    @pytest.fixture
    def search_invalid_filter_event(self) -> dict:
        """Event with an unsupported status as fitlter."""
        return load_json_event("event_invalid_filter")

    def test_valid_search(
        self,
        test_db_connection: Connection,
        test_data: None,
        search_all_event: dict,
        mocker: MockerFixture,
    ):
        """
        GIVEN a test database with a set of known records
        WHEN an event requesting the complete list of properties is received
        THEN a succesfull response with a list of known size of objects is returned
        """
        mocker.patch.object(Database, "connect", lambda: test_db_connection)
        response = handler(search_all_event, {})

        # parse body for efective assertions
        body = json.loads(response["body"])

        assert response["statusCode"] == StatusCodes.HTTP_200_OK
        assert isinstance(body, list)
        assert len(body) == 6

    def test_search_with_filters(
        self,
        test_db_connection: Connection,
        test_data: None,
        search_with_filters_event: dict,
        mocker: MockerFixture,
    ):
        """
        GIVEN a test database with a set of known records
        WHEN an event requesting properties that match a set of filters
        THEN a succesfull response with a list of known size of objects is returned
        """
        mocker.patch.object(Database, "connect", lambda: test_db_connection)
        mocker.patch("models.SQL_PLACEHOLDER", "?")
        response = handler(search_with_filters_event, {})

        # parse body for efective assertions
        body = json.loads(response["body"])

        assert response["statusCode"] == StatusCodes.HTTP_200_OK
        assert isinstance(body, list)
        assert len(body) == 1

    def test_method_not_allowed(
        self,
        test_db_connection: Connection,
        search_invalid_method_event: dict,
        mocker: MockerFixture,
    ):
        """
        GIVEN a test database
        WHEN an event with an invalid method
        THEN an error response with method not allowed status code is returned
        """
        mocker.patch.object(Database, "connect", lambda: test_db_connection)
        response = handler(search_invalid_method_event, {})

        assert response["statusCode"] == StatusCodes.HTTP_405_METHOD_NOT_ALLOWED

    def test_status_not_allowed(
        self,
        test_db_connection: Connection,
        search_invalid_status_event: dict,
        mocker: MockerFixture,
    ):
        """
        GIVEN a test database
        WHEN an event with an invalid status filter
        THEN an error response with bad request status code is returned
        """
        mocker.patch.object(Database, "connect", lambda: test_db_connection)
        response = handler(search_invalid_status_event, {})

        assert response["statusCode"] == StatusCodes.HTTP_400_BAD_REQUEST

    def test_filter_not_allowed(
        self,
        test_db_connection: Connection,
        search_invalid_filter_event: dict,
        mocker: MockerFixture,
    ):
        """
        GIVEN a test database
        WHEN an event with an invalid filter field
        THEN an error response with bad request status code is returned
        """
        mocker.patch.object(Database, "connect", lambda: test_db_connection)
        response = handler(search_invalid_filter_event, {})

        assert response["statusCode"] == StatusCodes.HTTP_400_BAD_REQUEST
