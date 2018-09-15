"""Pair opening and closing
"""
import json

from opening_hours.constants import DAYS_OF_WEEK
from opening_hours.request.clean.exceptions import CleanRequestError
from opening_hours.request.clean.utils import (
    is_closing_hour,
    is_opening_hour,
    get_or_throw_exception,
    get_next_day,
    get_previous_day,
)
from opening_hours.utils import split_to_pairs


def _validate_and_convert_hours_pair_to_dict(hours_pair):
    """Validate that hours pairs has correct format and convert to dict

    Check if first hour in pair is opening, second one is closing and
    opening hour is before closing hour.
    Throw error if any of these conditions are not matched.
    If validation succeeded converts hours to dict

    Args:
        hours_pair (list): List of two elements with format:
        [
            {
                'type': str, 'value': int
            }
        ]

    Returns:
        Dict with opening and closing hours. Format:
        {
            'open': int,
            'close': int
        }
    """
    # Raise error if pair size is invalid
    if len(hours_pair) != 2:
        raise CleanRequestError(
            'Found unmatched hours. {}'.format(json.dumps(hours_pair)))
    # Process pair with valid size
    opening_hour, closing_hour = hours_pair
    if not is_opening_hour(opening_hour) or \
            not is_closing_hour(closing_hour) or \
            opening_hour['value'] > closing_hour['value']:
        raise CleanRequestError(
            'Invalid opening and closing hours found. '
            'Opening hour should be before closing hour. '
            'Opening hour: {opening_hour}, Closing hour: {closing_hour}'.\
            format(
                opening_hour=opening_hour['value'],
                closing_hour=closing_hour['value']))
    return {
        'open': opening_hour['value'],
        'close': closing_hour['value']
    }


def _pair_opening_and_closing_hours(hours):
    """Group hours into pairs

    Store separately closing hour, if it is the first item in the list;
    and opening hour if it doesn't have pair.
    Throw CleanRequestError if otherwise can not create proper pairs.

    Args:
        hours (list): List of opening and closing hours for one day.
        Format:
        [
            {
                'type': str, 'value': int
            }
        ]

    Returns:
        Dict with paired opening and closing hours,
        and unmatched first closing hour and last opening hour if found.
        Format:
        {
            'hours': [
                {
                    'open': int,
                    'close': int
                }
            ],
            'unmatched_opening_hour': int,
            'unmatched_closing_hour': int
        }
    """
    # Check if first hour is unmatched closing hour
    unmatched_closing_hour = None
    if hours and is_closing_hour(hours[0]):
        # First hour type is closing. Apparently previous day was not closed
        unmatched_closing_hour = hours[0]['value']
        # Remove closing hours of previous day from list
        hours = hours[1:]
    # Check if last hour is unmatched opening hour
    unmatched_opening_hour = None
    if hours and is_opening_hour(hours[-1]):
        # Last hour type is closing. Apparently current day is not closed
        unmatched_opening_hour = hours[-1]['value']
        # Remove closing hours of previous day from list
        hours = hours[:-1]
    # Process other hours
    opening_and_closing_hour_pairs = split_to_pairs(hours)
    hour_pairs_as_dicts = list(map(
        _validate_and_convert_hours_pair_to_dict,
        opening_and_closing_hour_pairs))
    return {
        'hours': hour_pairs_as_dicts,
        'unmatched_opening_hour': unmatched_opening_hour,
        'unmatched_closing_hour': unmatched_closing_hour
    }


def pair_hours_for_each_day(days):
    """Group hours for each day in pairs of opening and closing hours

    First closing hour and last opening hour can be without pair,
    in case shift is open on one day and closed during the next day

    Args:
       days (dict): Valid dictionary with opening and closing hours by days.
       Format:
       {
            'day_of_week': [
                {
                    'type': str, 'value': int
                }
            ]
        }

    Returns:
        Dict with opening and closing hours grouped in pairs:
        {
            'day_of_week': {
                'hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ],
                'unmatched_opening_hour': int,
                'unmatched_closing_hour': int
            }
        }
    """
    days_processed = map(
        lambda day: (day[0], _pair_opening_and_closing_hours(day[1])),
        days.items())
    return dict(days_processed)


def _try_match_opening_and_closing_hour(opening_day, closing_day):
    """Attempt matching closing hours of the second day (closing day)
    with opening hours of the first day (opening day)

    Match opening hours to closing hours and add new pair to the first day
    (opening day). Throw error if hours can not be matched

    Args:
        opening_day (dict): Day with unmatched opening hour
        closing_day (dict): Day with unmatched closing hour
        Format: {
            'hours': [
                {
                    'open': int,
                    'close': int
                }
            ],
            'unmatched_opening_hour': int,
            'unmatched_closing_hour': int
        }

    Return:
        opening_day (dict): Updated first day with matched opening and closing hours
        Format:
        {
            'hours': [
                {
                    'open': int,
                    'close': int
                }
            ],
            'unmatched_opening_hour': None,
            'unmatched_closing_hour': int
        }
        closing_day (dict): Updated second day without unmatched closing hours
        Format:
        {
            'hours': [
                {
                    'open': int,
                    'close': int
                }
            ],
            'unmatched_opening_hour': int,
            'unmatched_closing_hour': None
        }
    """
    opening_hour = opening_day.get('unmatched_opening_hour', None)
    closing_hour = closing_day.get('unmatched_closing_hour', None)
    if not opening_hour or not closing_hour:
        raise CleanRequestError(
            'Unmatched opening and closing hours found. '
            'Opening hours: {opening_hour}. Closing hours: {closing_hour}.'.\
            format(
                opening_hour=opening_hour or 'Not found',
                closing_hour=closing_hour or 'Not found'
            ))
    new_shift = {
        'open': opening_hour,
        'close': closing_hour
    }
    opening_day_hours = opening_day['hours'] + [new_shift]
    return \
        {
            **opening_day,
            'unmatched_opening_hour': None,
            'hours': opening_day_hours
        }, \
        {
            **closing_day,
            'unmatched_closing_hour': None
        }


def pair_incomplete_hours_for_subsequent_days(days):
    """Pair unmatched opening and closing hours if found

    Pair unmatched opening hour with unmatched closing hour of the next day
    Throw CleanRequestError if can not create pairs.

    Args:
        days (dict): Dict with opening and closing hours
        for each day.
        Format:
        {
            'day_of_week': {
                'hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ],
                'unmatched_opening_hour': int,
                'unmatched_closing_hour': int
            }
        }

    Returns:
        Dict with complete pairs of opening and closing hours for each day
        Format:
        {
            'day_of_week': {
                'hours': [
                    {
                        'open': int,
                        'close': int
                    },
                ],
                'unmatched_opening_hour': None,
                'unmatched_closing_hour': None
            }
        }
    """
    for day_name in DAYS_OF_WEEK:
        day = get_or_throw_exception(day_name, days)
        # Try match opening hours with closing hours of the next day
        if day['unmatched_opening_hour']:
            next_day_name, next_day = get_next_day(day_name, days)
            day, next_day = _try_match_opening_and_closing_hour(day, next_day)
            days = {**days, next_day_name: next_day}
        # Try match closing hours with opening hours of the next day
        if day['unmatched_closing_hour']:
            previous_day_name, previous_day = get_previous_day(day_name, days)
            previous_day, day = \
                _try_match_opening_and_closing_hour(previous_day, day)
            days = {**days, previous_day_name: previous_day}
        days = {**days, day_name: day}
    return days
