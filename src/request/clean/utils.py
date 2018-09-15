"""Utility functions, related to request cleaning and aware of request format
"""
from src.request.clean.exceptions import CleanRequestError
from src.utils import (
    get_next_weekday_name,
    get_previous_weekday_name)


def is_closing_hour(hour):
    """Validate if hour is closing

    Args:
        hour (dict): Opening or closing hour with type an value. Format:
            {
                'type': str, 'value': int
            }

    Returns:
        Boolean flag, that shows if hour is closing
    """
    return hour['type'] == 'close'


def is_opening_hour(hour):
    """Validate if hour is open

    Args:
        hour (dict): Opening or closing hour with type an value. Format:
            {
                'type': str, 'value': int
            }

    Returns:
        Boolean flag, that shows if hour is closing
    """
    return hour['type'] == 'open'


def get_or_throw_exception(day_name, days):
    """Get day by name from days and throw exception if day was not found

    Args:
        day_name (str): Name of the day
        days (dict): Dict with days of week

    Return:
        day with day_name if found
    """
    try:
        return days[day_name]
    except KeyError:
        raise CleanRequestError(
            'Missing day: {day_name}'.\
            format(day_name=day_name))


def get_next_day(day_name, days):
    """Retrieve next weekday from days dict

    Args:
        day_name (str): Name of current weekday
        days (dict): Dict with all weekdays

    Return:
        next_day_name (str): Name of the next weekday
        next_day (dict): Next weekday retrieved from days dict
    """
    next_day_name = get_next_weekday_name(day_name)
    return next_day_name, get_or_throw_exception(next_day_name, days)


def get_previous_day(day_name, days):
    """Retrieve previous weekday from days dict

    Args:
        day_name (str): Name of current weekday
        days (dict): Dict with all weekdays

    Return:
        previous_day_name (str): Name of the previous weekday
        previous_day (dict): Previous weekday retrieved from days dict
    """
    previous_day_name = get_previous_weekday_name(day_name)
    return previous_day_name, get_or_throw_exception(previous_day_name, days)
