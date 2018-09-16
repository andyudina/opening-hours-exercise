"""Format restaurant opening hours
"""
from jsonschema import ValidationError

from src.request.query import get_query_param, QueryError
from src.request.parse import decode_and_load_json, ParseError
from src.request.validate import validate_request
from src.response import (
    create_bad_request_response,
    create_successfull_resonse,
    create_unprocessable_entity_response
)
from src.working_hours import Week, WorkingHoursError


def handler(event, _):
    """Main API handler.

    Convert opening hours from request to human readable format

    Args:
        event (dict): Request in format of API Gateway
        Expected to be have this format:
        {
            'queryStringParameters': {
                'query': str
            }
        ]
        Query is base64 encoded JSON with opening hours

    Returns:
        Response dict. Format:
        {
            'statusCode': int,
            'body': str
        }
        "body" is JSON with result of the response.
        Successful response:
        {
            'working_hours': str
        }
        Error response:
        {
            'error': str
        }
    """
    try:
        request = get_query_param(event, 'query')
        decoded_request = decode_and_load_json(request)
        validate_request(decoded_request)
    except (QueryError, ParseError, ValidationError) as err:
        return create_bad_request_response(err.message)
    # We do not catch KeyError from get_query_param on purpose here
    # We want to fail fast if event format has changed
    # 500 server error response and logging will be handled by AWS Lambda
    try:
        working_hours_in_human_readable_format = Week.\
            create_week_from_json(decoded_request).\
            to_human_readable_format()
    except WorkingHoursError as err:
        return create_unprocessable_entity_response(err.message)
    response_body = {
        'working_hours': working_hours_in_human_readable_format
    }
    return create_successfull_resonse(response_body)
