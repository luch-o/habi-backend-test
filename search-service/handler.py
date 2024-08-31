"""This module takes care of processing the request and returning a response."""

import json

from controller import parse_errors, search_properties, validate_request
from exceptions import ApplicationError


def handler(event, context):
    """Lambda function handler."""
    body = json.loads(event["body"]) if "body" in event else {}
    try:
        validate_request(event)
        filters = body.get("filters", {})
        status_code, body = search_properties(filters)
    except ApplicationError as e:
        status_code, body = parse_errors(e)

    response = {
        "statusCode": status_code.value,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }

    return response
