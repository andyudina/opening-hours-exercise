"""Print opening hours in human readable format
"""
from opening_hours.utils import print_time


def _create_working_hours_str_for_closed_day():
    """Create working hours description for day when restaurant is closed
    """
    return 'Closed'

def _create_str_with_working_hours(working_hours):
    """Create working hours description

    Args:
        hours (list): List of working hours for one day
        Format:
        [
            {
                'open': int,
                'close': int
            }
        ]

    Return:
        String with working hours. For example: "8 AM - 1 PM, 6 PM - 1 PM"
    """
    def _create_str_for_one_shift(shift):
        """
        Create description for one shift.
        """
        return '{opening_hour} - {closing_hour}'.format(
            opening_hour = print_time(shift['open']),
            closing_hour = print_time(shift['close'])
        )
    return ', '.join([
        _create_str_for_one_shift(shift)
        for shift in working_hours
    ])

def _print_working_hours_for_one_day(day):
    """Print working hours for one day in human readable format

    Args:
        day (dict): Weekday with working hours
        Format:
        {
            'day_of_week': str,
            'hours': [
                {
                    'open': int,
                    'close': int
                }
            ],
            'is_open': boolean
        }

    Return:
        String with working hours for current day.
        For example: "Monday: 8 AM - 1 PM, 6 PM - 1 PM"
    """
    day_of_week = day['day_of_week'].capitalize()
    if day['is_open']:
        working_hours = _create_str_with_working_hours(day['hours'])
    else:
        working_hours = _create_working_hours_str_for_closed_day()
    return '{day_of_week}: {working_hours}'.format(
        day_of_week = day_of_week,
        working_hours = working_hours)

def print_opening_hours(days):
    """Print opening hours to string in human readable format

    Args:
        days (list): List of weekdays with opening and closing hours.
        Format:
        [
            {
                'day_of_week': str,
                'hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ],
                'is_open': boolean
            }
        ]

    Return:
        String with working hours by days, separated with new line.
    """
    return '\n'.join(
        [
            _print_working_hours_for_one_day(day)
            for day in days
        ]
    )
