"""Test case for request.query.get_query_param
"""
import unittest

from opening_hours.request.query import get_query_param, QueryError


class TestGetQueryParam(unittest.TestCase):
    """Test request.query.get_query_param function
    """

    def test_param_value_return(self):
        """
        Param value returned if found
        """
        request = {
            'queryStringParameters': {
                'test-param': 'test-value'
            }
        }
        self.assertEqual(
            get_query_param(request, 'test-param'), 'test-value')

    def test_raise_query_error_if_param_does_not_exist(self):
        """
        Raise error if query param not found
        """
        request = {
            'queryStringParameters': {
                'not-a-test-param': 'test-value'
            }
        }
        with self.assertRaises(QueryError):
            get_query_param(request, 'test-param')

    def test_raise_query_error_if_query_string_is_empty(self):
        """
        Raise error if query string is empty
        """
        request = {
            'queryStringParameters': None
        }
        with self.assertRaises(QueryError):
            get_query_param(request, 'test-param')

    def test_raise_key_error_if_request_format_is_invalid(self):
        """
        Raise key error if query string parameters are missing in request.

        Request dict is being formed by AWS platform.
        If query string key is missing in request it's better to fail fast
        with original KeyError, cause it means that specification has changed
        (or bug on AWS side) and whole service is down.
        """
        request = {}
        with self.assertRaises(KeyError):
            get_query_param(request, 'test-param')
