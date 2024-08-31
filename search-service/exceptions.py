"""Custom exceptions module."""

from httputil import StatusCodes
from models import Status


class ApplicationError(Exception):
    status_code: StatusCodes
    message: str


class UnsupportedMethodError(ApplicationError):
    """Raise for unsupported HTTP methods."""

    status_code = StatusCodes.HTTP_405_METHOD_NOT_ALLOWED
    message = None


class BadFilterError(ApplicationError):
    """Raise for bad requests."""

    status_code = StatusCodes.HTTP_400_BAD_REQUEST


class UsupportedFilterError(BadFilterError):
    """Raise for trying to seatch by an unsupported status."""

    default_mesage = "invalid filters, only year, city and status are allowed."

    def __init__(self):
        super().__init__()
        self.message = self.default_mesage


class UnsupportedStatusError(BadFilterError):
    """Raise for trying to search by an supported field."""

    default_message = (
        "Invalid status. Got {received_status}. Supported are {supported_status}"
    )

    def __init__(self, actual_status: str):
        super().__init__()
        self.message = self.default_message.format(
            **{
                "received_status": actual_status,
                "supported_status": ", ".join([status for status in Status]),
            }
        )
