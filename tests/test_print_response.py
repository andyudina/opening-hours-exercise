"""Test case for response.print function
"""
import unittest

from opening_hours.response.print import print_opening_hours


class TestPrintOpeningHours(unittest.TestCase):
    """Test printing opening hours in human readable format
    """

    def test_print_opening_hours_for_day_when_restaurant_is_closed(self):
        """
        Print valid message for day when restaurant is closed
        """
        days = [
            {
                'day_of_week': 'saturday',
                'hours': [],
                'is_open': False
            }
        ]
        expected_message = 'Saturday: Closed\n'
        self.assertEqual(print_opening_hours(days), expected_message)

    def test_print_opening_hours_for_multiple_days(self):
        """
        Print valid message for multiple days
        """
        days = [
            {
                'day_of_week': 'tuesday',
                'hours': [
                    {
                        'open': 36000,
                        'close': 64800
                    }
                ],
                'is_open': True
            },
            {
                'day_of_week': 'wednesday',
                'hours': [
                    {
                        'open': 36000,
                        'close': 64800
                    }
                ],
                'is_open': True
            }
        ]
        expected_message = 'Tuesday: 10 AM - 6 PM\nWednesday: 10 AM - 6 PM\n'
        self.assertEqual(print_opening_hours(days), expected_message)

    def test_multiple_shifts_in_one_day_are_printed_successfully(self):
        """
        Print valid message for multiple shifts in one day
        """
        days = [
            {
                'day_of_week': 'Monday',
                'hours': [
                    {
                        'open': 21600,
                        'close': 39600
                    },
                    {
                        'open': 57600,
                        'close': 75600
                    }
                ],
                'is_open': True
            },
        ]
        expected_message = 'Monday: 8 AM - 1 PM, 6 PM - 1 PM\n'
        self.assertEqual(print_opening_hours(days), expected_message)
