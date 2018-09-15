"""Format restaurant opening hours
"""
import json
import http
from jsonschema import ValidationError

from src.request.clean import clean, CleanRequestError
from src.request.query import get_query_param, QueryError
from src.request.parse import decode_and_load_json, ParseError
from src.request.validate import validate_request
from src.response.print import print_opening_hours


def _create_response(status_code, body):
    """Create response with status code and body from args
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


def _create_error_response(status_code, error_message):
    """Create response with status code from args request
    and JSON body: { "error": error_message }
    """
    body = {
        'error': error_message
    }
    return _create_response(status_code, body)


def _create_bad_request_response(error_message):
    """Create response with status code 400 bad request
    and JSON body: { "error": error_message }
    """
    return _create_error_response(
        status_code=http.HTTPStatus.BAD_REQUEST, error_message=error_message)


def _create_unprocessable_entity_response(error_message):
    """Create response with status code 422 unprocessable entity
    and JSON body: { "error": error_message }
    """
    return _create_error_response(
        status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        error_message=error_message)


def _create_successfull_resonse(body):
    """Create response with status code 200 ok
    and JSON body received as argument
    """
    return _create_response(
        status_code=http.HTTPStatus.OK, body=body)


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
        return _create_bad_request_response(err.message)
    # We do not catch KeyError from get_query_param on purpose here
    # We want to fail fast if event format has changed
    # 500 server error response and logging will be handled by AWS Lambda
    try:
        working_hours = clean(decoded_request)
    except CleanRequestError as err:
        return _create_unprocessable_entity_response(err.message)
    response_body = {
        'working_hours': print_opening_hours(working_hours)
    }
    return _create_successfull_resonse(response_body)
