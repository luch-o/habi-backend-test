"""This module includes business logic with error handling"""

from exceptions import (
    ApplicationError,
    UnsupportedMethodError,
    UnsupportedStatusError,
    UsupportedFilterError,
)
from httputil import ALLOWED_METHODS, StatusCodes
from models import Property, Status
from serializers import PropertySerializer


def validate_request(event: dict) -> bool:
    """Validate allowd method in request."""
    method = event.get("requestContext", {}).get("http", {}).get("method")
    if method not in ALLOWED_METHODS:
        raise UnsupportedMethodError()


def search_properties(filters: dict[str, str | int]) -> tuple[int, dict | list[dict]]:
    """Search properties with error handling.

    Returns status code and body for response."""
    try:
        if "status" in filters:
            filters["status"] = Status(filters.get("status"))
        properties = Property.search(**filters)
        status_code = StatusCodes.HTTP_200_OK
        body = [PropertySerializer.to_dict(p) for p in properties]

    except TypeError:
        raise UsupportedFilterError()
    except ValueError:
        raise UnsupportedStatusError(filters.get("status"))

    return status_code, body


def parse_errors(exc: ApplicationError) -> tuple[StatusCodes, dict]:
    """Returns the response status code and body for a given exception."""
    status_code = exc.status_code
    body = {"message": exc.message} if exc.message is not None else {}
    return status_code, body
