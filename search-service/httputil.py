"""This module includes constants used for http event handling."""

from enum import IntEnum

ALLOWED_METHODS = frozenset(("GET", "HEAD"))


class StatusCodes(IntEnum):
    HTTP_200_OK = 200
    HTTP_400_BAD_REQUEST = 400
    HTTP_405_METHOD_NOT_ALLOWED = 405
