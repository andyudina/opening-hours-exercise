"""Miscellaneous utility functions
"""
import time
from first import first

from src.constants import (
    DAYS_OF_WEEK,
    DAYS_OF_WEEK_WITH_ORDER)


def split_to_pairs(seq):
    """Split list into sublists with length == 2
    Args:
        seq (list): List to be split
    Returns:
        List of sublists with
    """
    size = 2
    return [seq[i:i + size] for i in range(0, len(seq), size)]


def get_next_weekday_name(day_name):
    """Get name of next weekday
    Throws KeyError if day_name is not valid weekday name
    Args:
        day_name (str): Name of current weekday.
        Accepted names: 'monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday'
    Returns:
        Name of the next weekday
    """
    current_day_index = DAYS_OF_WEEK_WITH_ORDER[day_name]
    next_day_index = current_day_index + 1
    if next_day_index >= len(DAYS_OF_WEEK):
        next_day_index = 0
    return DAYS_OF_WEEK[next_day_index]


def get_previous_weekday_name(day_name):
    """Get name of previous weekday
    Throws KeyError if day_name is not valid weekday name
    Args:
        day_name (str): Name of current weekday
        Accepted names: 'monday', 'tuesday', 'wednesday', 'thursday',
                        'friday', 'saturday', 'sunday'
    Returns:
        Name of the previous weekday
    """
    current_day_index = DAYS_OF_WEEK_WITH_ORDER[day_name]
    next_day_index = current_day_index - 1
    return DAYS_OF_WEEK[next_day_index]


def print_time(timestamp):
    """Print time in 12-hour clock format
    Args:
        timestamp (int): Unix time (1.1.1970 as date)
    Return:
        String, representing current time, in 12-hour clock format
    """
    _time = time.gmtime(timestamp)
    hour = int(time.strftime('%I', _time))
    return '{hour} {period}'.format(
        hour=hour,
        period=time.strftime('%p', _time)
    )


def _filter_empty_keys(dict_):
    """Filter out keys from dict which values are None
    """
    return {
        key: value
        for key, value in dict_.items()
        if value is not None
    }


def filter_dict_items(dict_, condition):
    """Create new dict using keys and values pairs from *dict_*,
    which values meet *condition*

    Expects *dict_* to have lists as values. Filters these lists
    using *condition* function and replaces list with first found element that
    matched the *condition*. Removes key, if "value" list doesn't have matching
    elements.

    Args:
        - dict_ : Dict with format:
        {
            'key': [
                'value'
            ]
        }
        - condition (function): Function, that accepts one argument
        and returns boolean flag. Is executed on every item of "value" list

    Returns:
        Updated dict with filtered keys and values
    """
    updated_dict = {
        key: first(
            [value for value in values if condition(value)]
        )
        for key, values in dict_.items()
    }
    return _filter_empty_keys(updated_dict)
