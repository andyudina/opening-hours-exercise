"""Utility functions, related to working hours processing
and aware of working hours format
"""
from src.working_hours.constants import (
    WEEKDAYS,
    WEEKDAYS_WITH_ORDER)
from src.working_hours.exceptions import WorkingHoursError


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
        raise WorkingHoursError(
            'Missing day: {day_name}'.
            format(day_name=day_name))


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
    current_day_index = WEEKDAYS_WITH_ORDER[day_name]
    next_day_index = current_day_index + 1
    if next_day_index >= len(WEEKDAYS):
        next_day_index = 0
    return WEEKDAYS[next_day_index]


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
