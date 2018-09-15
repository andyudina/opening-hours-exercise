"""Test case for request parsing
"""
import unittest

from opening_hours.request.parse import decode_and_load_json, ParseError


class TestParseRequest(unittest.TestCase):
    """Test request parsing with json schema
    """

    def test_valid_request_passed(self):
        """
        Valid request passes validation
        """
        request = 'eyJ0ZXN0IjogInRlc3QifQ=='  # { "test": "test" }
        self.assertEqual(
            decode_and_load_json(request), {'test': 'test'})

    def test_parse_error_raised_if_base64_encoding_is_invalid(self):
        """
        Raise ParseError if can not decode base64
        """
        request = 'invalid-base-64'
        with self.assertRaises(ParseError):
            decode_and_load_json(request)

    def test_parse_error_raised_if_json_is_invalid(self):
        """
        Raise ParseError if can not parse JSON
        """
        request = 'eyJ0ZXN0IjogInRlc3QifX0='  # {"test": "test"}}
        with self.assertRaises(ParseError):
            decode_and_load_json(request)
