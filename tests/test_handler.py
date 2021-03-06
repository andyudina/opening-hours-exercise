"""Test main handler
"""
import base64
import json
import unittest

from src.handler import handler


def generate_response(status_code, body):
    """Help to generated expected response from handler
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


def generate_request(payload):
    """Help to generate request to lambda handler
    """
    return {
        'queryStringParameters': {
            'query': base64.b64encode(json.dumps(payload).encode())
        }
    }


class TestMainHandler(unittest.TestCase):
    """Test main handler response
    """

    def test_valid_request(self):
        """
        We return 200 OK and working hours in human readable format
        if request is successful
        """
        request_payload = {
            'monday': [],
            'tuesday': [
                {
                    'type': 'open',
                    'value': 36000
                },
                {
                    'type': 'close',
                    'value': 64800
                }
            ],
            'wednesday': [],
            'thursday': [
                {
                    'type': 'open',
                    'value': 36000
                },
                {
                    'type': 'close',
                    'value': 64800
                }
            ],
            'friday': [
                {
                    'type': 'open',
                    'value': 36000
                },
            ],
            'saturday': [
                {
                    'type': 'close',
                    'value': 3600
                },
                {
                    'type': 'open',
                    'value': 36000
                },
            ],
            'sunday': [
                {
                    'type': 'close',
                    'value': 3600
                },
                {
                    'type': 'open',
                    'value': 43200
                },
                {
                    'type': 'close',
                    'value': 75600
                }
            ]
        }
        request = generate_request(payload=request_payload)
        response = handler(request, None)
        expected_response_body = {
            'working_hours': [
                'Monday: Closed',
                'Tuesday: 10 AM - 6 PM',
                'Wednesday: Closed',
                'Thursday: 10 AM - 6 PM',
                'Friday: 10 AM - 1 AM',
                'Saturday: 10 AM - 1 AM',
                'Sunday: 12 PM - 9 PM'
            ]
        }
        expected_response = generate_response(
            status_code=200,
            body=expected_response_body)
        self.assertEqual(response, expected_response)

    def test_invalid_request_format(self):
        """
        We return 400 bad request and error message
        if request format is invalid
        """
        request_payload = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
        }
        request = generate_request(payload=request_payload)
        response = handler(request, None)
        expected_response_body = {
            'error': '\'sunday\' is a required property'
        }
        expected_response = generate_response(
            status_code=400,
            body=expected_response_body)
        self.assertEqual(response, expected_response)

    def test_create_week_failed(self):
        """
        We return 422 unprocessable entity and error message
        if we can not create week from json in request
        """
        request_payload = {
            'monday': [],
            'tuesday': [],
            'wednesday': [],
            'thursday': [],
            'friday': [],
            'saturday': [],
            'sunday': [
                {
                    'type': 'close',
                    'value': 3600
                },
                {
                    'type': 'open',
                    'value': 43200
                },
            ]
        }
        request = generate_request(payload=request_payload)
        response = handler(request, None)
        expected_response_body = {
            'error': 'Missing day: monday'
        }
        expected_response = generate_response(
            status_code=422,
            body=expected_response_body)
        self.assertEqual(response, expected_response)

    def test_parse_request_failed(self):
        """
        We return 400 bad request and error message
        if request can not be parsed
        """
        request = {
            'queryStringParameters': {
                'query': 'invalid-base-64'
            }
        }
        response = handler(request, None)
        expected_response_body = {
            'error': 'Invalid base64 format'
        }
        expected_response = generate_response(
            status_code=400,
            body=expected_response_body)
        self.assertEqual(response, expected_response)

    def test_query_is_missing(self):
        """
        We return 400 bad request and error message
        if query is missing
        """
        request = {
            'queryStringParameters': {}
        }
        response = handler(request, None)
        expected_response_body = {
            'error': 'Query parameter "query" is missing'
        }
        expected_response = generate_response(
            status_code=400,
            body=expected_response_body)
        self.assertEqual(response, expected_response)
