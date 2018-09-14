"""Test case for request validation
"""
import unittest
from jsonschema import ValidationError

from opening_hours.request.validate import validate_request
from tests.utils import (
    generate_empty_request,
    generate_valid_request)


class TestValidateRequest(unittest.TestCase):
    """Test request validation with json schema
    """

    def test_valid_request_passed(self):
        """
        Valid request passes validation
        """
        request = generate_valid_request()
        validate_request(request)

    def test_valid_request_with_empty_working_hours_passed(self):
        """
        Valid request with empty working hours passes validation
        """
        request = generate_empty_request()
        validate_request(request)

    def test_raise_error_if_day_is_missing(self):
        """
        Raise error if one weekday is missing
        """
        request = generate_valid_request()
        request.pop('monday', None)
        with self.assertRaises(ValidationError):
            validate_request(request)

    def test_raise_error_if_working_hours_format_is_invalid(self):
        """
        Raise error if working hours format is invalid
        """
        request = generate_valid_request()
        request['monday'] = [
            {
                'type': 'open'
            }
        ]
        with self.assertRaises(ValidationError):
            validate_request(request)

    def test_raise_error_if_working_hours_type_is_invalid(self):
        """
        Raise error if working hours type is not open or close
        """
        request = generate_valid_request()
        request['monday'] = [
            {
                'type': 'not-valid',
                'value': 0
            }
        ]
        with self.assertRaises(ValidationError):
            validate_request(request)

    def test_raise_error_if_working_hours_value_is_invalid(self):
        """
        Raise error if working hour value is more than 86399 (11.59:59 PM)
        """
        request = generate_valid_request()
        request['monday'] = [
            {
                'type': 'open',
                'value': 90000
            }
        ]
        with self.assertRaises(ValidationError):
            validate_request(request)
