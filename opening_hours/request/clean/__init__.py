"""Clean opening hours 
"""
from opening_hours.constants import DAYS_OF_WEEK
from opening_hours.request.clean.pair import (
    pair_hours_for_each_day,
    pair_incomplete_hours_for_subsequent_days,
)

# CleanRequestError should be imported from opening_hours.request.clean module
from opening_hours.request.clean.errors import CleanRequestError

def _format_hours(days):
    """Transform opening hours of each day to easy printable format

    Args:
        days (dict): Dict with opening and closing hours for each day.
        Format:
        {
            'day_of_week': {
                'hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ]
            }
        }

    Returns:
        List of opening hours by days. Format:
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
    """
    def _format_one_day(day_name, day):
        """Transform one day to easy printable format
        """
        return {
            'day_of_week': day_name,
            'hours': day['hours'],
            'is_open': len(day['hours']) > 0
        }

    days_formated = map(
        lambda day_name: _format_one_day(day_name, days[day_name]),
        DAYS_OF_WEEK)
    return list(days_formated)

def clean(days):
    """Transform JSON request with opening hours to simplify further processing

    Args:
       days (dict): Valid dictionary with opening hours:
       Format:
       { 
            'day_of_week': [
                {
                    'type': str, 'value': int
                }
            ] 
        }

    Returns:
        List of opening hours by days. Format:
        [
            {
                'day_of_week': str,
                'opening_hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ],
                'is_open': boolean
            }
        ]
    """
    # Group opening and closing hours into pairs
    days_with_hours_in_pairs = pair_hours_for_each_day(days)
    # Complete shifts that start at one day and end during the next day
    days_completed = \
        pair_incomplete_hours_for_subsequent_days(days_with_hours_in_pairs)
    # Change day format adding is_open flag and day of week name
    return _format_hours(days_completed)
