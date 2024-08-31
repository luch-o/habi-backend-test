"""This module includes utilities used for http event handling."""

from enum import IntEnum


class StatusCodes(IntEnum):
    HTTP_200_OK = 200
    HTTP_400_BAD_REQUEST = 400
    HTTP_405_METHOD_NOT_ALLOWED = 409


def validate_request(event: dict) -> bool:
    """Validate GET method in request."""
    method = event.get("requestContext", {}).get("http", {}).get("method")
    return method == "GET"
