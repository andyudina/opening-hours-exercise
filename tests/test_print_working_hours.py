"""Test case for response.print function
"""
import unittest

from src.working_hours import Week, Weekday, Shift
from src.working_hours.constants import WEEKDAYS


def print_working_hours(days):
    """Help to create week with days and shifts,
    and convert to human readable format.

    Args:
        days (list): Weekdays in format:
        [
            {
                'day_of_week': str,
                'hours': [
                    {
                        'open': int,
                        'close': int,
                    }
                ]
            }
        ]
    """
    weekdays = {}
    for day in days:
        shifts = []
        for hour in day['hours']:
            shifts.append(
                Shift(open_hour=hour['open'], close_hour=hour['close'])
            )
        weekdays[day['day_of_week']] = \
            Weekday(name=day['day_of_week'], shifts=shifts)
    return Week(**weekdays).to_human_readable_format()


class TestPrintOpeningHours(unittest.TestCase):
    """Test printing opening hours in human readable format
    """

    def test_print_working_hours_for_day_when_restaurant_is_closed(self):
        """
        Print valid message for day when restaurant is closed
        """
        days = [
            {
                'day_of_week': 'saturday',
                'hours': [],
            }
        ]
        expected_message = 'Saturday: Closed'
        self.assertEqual(print_working_hours(days), expected_message)

    def test_print_working_hours_for_multiple_days(self):
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
            },
            {
                'day_of_week': 'wednesday',
                'hours': [
                    {
                        'open': 36000,
                        'close': 64800
                    }
                ],
            }
        ]
        expected_message = 'Tuesday: 10 AM - 6 PM\nWednesday: 10 AM - 6 PM'
        self.assertEqual(print_working_hours(days), expected_message)

    def test_multiple_shifts_in_one_day_are_printed_successfully(self):
        """
        Print valid message for multiple shifts in one day
        """
        days = [
            {
                'day_of_week': 'monday',
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
            },
        ]
        expected_message = 'Monday: 6 AM - 11 AM, 4 PM - 9 PM'
        self.assertEqual(print_working_hours(days), expected_message)
