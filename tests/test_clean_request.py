"""Test case for request.clean function
"""
import unittest

from src.request.clean import clean, CleanRequestError
from src.constants import DAYS_OF_WEEK
from tests.utils import generate_empty_request


def generate_empty_response():
    """
    Help to generate cleaned request where all days don't have
    opening or closing hours
    """
    return [
        {
            'day_of_week': day_of_week,
            'hours': [],
            'is_open': False
        }
        for day_of_week in DAYS_OF_WEEK
    ]


def update_response_list(response, updates):
    """
    Help to update response items with information from updates list
    Merges using day_of_name as a key
    """
    updates_dict = {update['day_of_week']: update for update in updates}
    return [
        updates_dict.get(day['day_of_week'], day)
        for day in response
    ]


class TestCleanOpeningHours(unittest.TestCase):
    """Test processing opening hours request
    """

    def test_empty_hours_processed_successfully(self):
        """
        Days when restaurant is closed are processed successfully
        """
        hours = generate_empty_request()
        expected_result = generate_empty_response()
        self.assertEqual(clean(hours), expected_result)

    def test_multiple_hours_during_same_day_processed_successfully(self):
        """
        Days when restaurant is open in multiple timeframes
        are processed successfully
        """
        hours = {
            **generate_empty_request(),
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
                'hours': [
                    {
                        'open': 32400,
                        'close': 39600,
                    },
                    {
                        'open': 57600,
                        'close': 82800,
                    }
                ],
                'is_open': True
            }
        ]
        expected_result = update_response_list(
            generate_empty_response(),
            expected_result)
        self.assertEqual(clean(hours), expected_result)

    def test_closing_on_the_next_day_processed_successfully(self):
        """
        Days when restaurant closes on the next day are processed
        successfully
        """
        hours = {
            **generate_empty_request(),
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
                'hours': [
                    {
                        'open': 82800,
                        'close': 32400,
                    }
                ],
                'is_open': True
            },
            {
                'day_of_week': 'saturday',
                'hours': [],
                'is_open': False
            }
        ]
        expected_result = update_response_list(
            generate_empty_response(),
            expected_result)
        self.assertEqual(clean(hours), expected_result)

    def test_sunday_with_closing_on_monday_processed_successfully(self):
        """
        Restaurant shift with shift that is opened on sunday
        and closed on moday is processed successfully
        """
        hours = {
            **generate_empty_request(),
            'sunday': [
                {
                    'type': 'open',
                    'value': 82800,
                }
            ],
            'monday': [
                {
                    'type': 'close',
                    'value': 32400,
                }
            ]
        }
        expected_result = [
            {
                'day_of_week': 'monday',
                'hours': [],
                'is_open': False
            },
            {
                'day_of_week': 'sunday',
                'hours': [
                    {
                        'open': 82800,
                        'close': 32400,
                    }
                ],
                'is_open': True
            },
        ]
        expected_result = update_response_list(
            generate_empty_response(),
            expected_result)
        self.assertEqual(clean(hours), expected_result)

    def test_days_of_week_are_in_the_right_order(self):
        """
        Days of week are stored in the right order: from monday to sunday
        """
        hours = {
            **generate_empty_request(),
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
                'hours': [
                    {
                        'open': 57600,
                        'close': 82800,
                    }
                ],
                'is_open': True
            },
            {
                'day_of_week': 'saturday',
                'hours': [
                    {
                        'open': 57600,
                        'close': 82800,
                    }
                ],
                'is_open': True
            },
        ]
        expected_result = update_response_list(
            generate_empty_response(),
            expected_result)
        self.assertEqual(clean(hours), expected_result)

    def test_error_is_thrown_if_closing_hours_are_not_found(self):
        """
        Error is thrown if no closing hours found
        """
        hours = {
            **generate_empty_request(),
            'friday': [
                {
                    'type': 'open',
                    'value': 57600,
                }
            ]
        }
        with self.assertRaises(CleanRequestError):
            clean(hours)

    def test_error_is_thrown_if_hours_are_not_found(self):
        """
        Error is thrown if no opening hours found
        """
        hours = {
            **generate_empty_request(),
            'friday': [
                {
                    'type': 'close',
                    'value': 57600,
                }
            ]
        }
        with self.assertRaises(CleanRequestError):
            clean(hours)

    def test_error_is_thrown_if_multiple_hours_of_the_same_type_are_found(
            self):
        """
        Error is thrown if multiple opening hours found one after another
        """
        hours = {
            **generate_empty_request(),
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
            clean(hours)
