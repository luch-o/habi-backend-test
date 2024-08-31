"""This module takes care of processing the request and returning a response."""

import json

from httputil import StatusCodes, validate_request
from models import Property, Status
from serializers import PropertySerializer


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
        status_code = StatusCodes.HTTP_400_BAD_REQUEST
        body = {"mesage": "invalid filters, only year, city and status are allowed."}
    except ValueError:
        status_code = StatusCodes.HTTP_400_BAD_REQUEST
        body = {
            "message": f"Invalid status. Got {filters.get('status')}. Supported are {[status.value for status in Status]}"
        }

    return status_code, body


def handler(event, context):
    """ "Lambda function handler."""
    if validate_request(event):
        body = json.loads(event["body"]) if "body" in event else {}
        filters = body.get("filters", {})
        status_code, body = search_properties(filters)
    else:
        status_code = StatusCodes.HTTP_405_METHOD_NOT_ALLOWED

    response = {
        "statusCode": status_code.value,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }

    return response
