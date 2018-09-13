"""Test case for request.clean function
"""
import unittest
from time import gmtime

from opening_hours.request.clean import clean, CleanRequestError


class TestCleanOpeningHours(unittest.TestCase):
    """Test processing opening hours request
    """

    def test_empty_opening_hours_processed_successfully(self):
        """
        Days when restaurant is closed are processed successfully
        """
        opening_hours = {
            'friday': []
        }
        expected_result = [
            {
                'day_of_week': 'friday',
                'opening_hours': [],
                'is_open': False
            }
        ]
        self.assertEqual(clean(opening_hours), expected_result)

    def test_multiple_hours_during_same_day_processed_successfully(self):
        """
        Days when restaurant is open in multiple timeframes
        are processed successfully
        """
        opening_hours = {
            'friday': [
                {
                    'type': 'open',
                    'value': 32400,
                },
                {
                    'type': 'close',
                    'value': 39600,
                },
                {
                    'type': 'open',
                    'value': 57600,
                },
                {
                    'type': 'close',
                    'value': 82800,
                },
            ]
        }
        expected_result = [
            {
                'day_of_week': 'friday',
                'opening_hours': [
                    {
                        'open': gmtime(32400),
                        'close': gmtime(39600),
                    },
                    {
                        'open': gmtime(57600),
                        'close': gmtime(82800),
                    }
                ],
                'is_open': True
            }
        ]
        self.assertEqual(clean(opening_hours), expected_result)

    def test_closing_on_the_next_day_processed_successfully(self):
        """
        Days when restaurant closes on the next day are processed
        successfully
        """
        opening_hours = {
            'friday': [
                {
                    'type': 'open',
                    'value': 82800,
                }
            ],
            'saturday': [
                {
                    'type': 'close',
                    'value': 32400,
                }
            ]
        }
        expected_result = [
            {
                'day_of_week': 'friday',
                'opening_hours': [
                    {
                        'open': gmtime(82800),
                        'close': gmtime(32400),
                    }
                ],
                'is_open': True
            }
        ]
        self.assertEqual(clean(opening_hours), expected_result)

    def test_days_of_week_are_in_the_right_order(self):
        """
        Days of week are stored in the right order: from monday to sunday
        """
        opening_hours = {
            'friday': [
                {
                    'type': 'open',
                    'value': 57600,
                },
                {
                    'type': 'close',
                    'value': 82800,
                }
            ],
            'saturday': [
                {
                    'type': 'open',
                    'value': 57600,
                },
                {
                    'type': 'close',
                    'value': 82800,
                }
            ]
        }
        expected_result = [
            {
                'day_of_week': 'friday',
                'opening_hours': [
                    {
                        'open': gmtime(57600),
                        'close': gmtime(82800),
                    }
                ],
                'is_open': True
            },
            {
                'day_of_week': 'saturday',
                'opening_hours': [
                    {
                        'open': gmtime(57600),
                        'close': gmtime(82800),
                    }
                ],
                'is_open': True
            },
        ]
        self.assertEqual(clean(opening_hours), expected_result)

    def test_error_is_thrown_if_closing_hours_are_not_found(self):
        """
        Error is thrown if no closing hours found
        """
        opening_hours = {
            'friday': [
                {
                    'type': 'open',
                    'value': 57600,
                }
            ]
        }
        with self.assertRaises(CleanRequestError):
            clean(opening_hours)

    def test_error_is_thrown_if_opening_hours_are_not_found(self):
        """
        Error is thrown if no opening hours found
        """
        opening_hours = {
            'friday': [
                {
                    'type': 'close',
                    'value': 57600,
                }
            ]
        }
        with self.assertRaises(CleanRequestError):
            clean(opening_hours)

    def test_error_is_thrown_if_multiple_hours_of_the_same_type_are_found(self):
        """
        Error is thrown if multiple opening hours found one after another
        """
        opening_hours = {
            'friday': [
                {
                    'type': 'close',
                    'value': 57600,
                },
                {
                    'type': 'close',
                    'value': 57600,
                }
            ]
        }
        with self.assertRaises(CleanRequestError):
            clean(opening_hours)
