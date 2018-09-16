"""Helpers to create response dict
"""
import json
import http


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


def create_bad_request_response(error_message):
    """Create response with status code 400 bad request
    and JSON body: { "error": error_message }
    """
    return _create_error_response(
        status_code=http.HTTPStatus.BAD_REQUEST, error_message=error_message)


def create_unprocessable_entity_response(error_message):
    """Create response with status code 422 unprocessable entity
    and JSON body: { "error": error_message }
    """
    return _create_error_response(
        status_code=http.HTTPStatus.UNPROCESSABLE_ENTITY,
        error_message=error_message)


def create_successfull_resonse(body):
    """Create response with status code 200 ok
    and JSON body received as argument
    """
    return _create_response(
        status_code=http.HTTPStatus.OK, body=body)
