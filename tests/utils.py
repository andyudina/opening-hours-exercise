"""Misc utils for tests
"""
from src.constants import DAYS_OF_WEEK


def generate_empty_request():
    """
    Help to generate request where all days don't have
    opening or closing hours
    """
    return {day_of_week: [] for day_of_week in DAYS_OF_WEEK}


def generate_valid_request():
    """
    Help to generate requests where all days have
    valid opening and closing hours
    """
    return {
        day_of_week: [
            {
                'type': 'open',
                'value': 32400,
            },
            {
                'type': 'close',
                'value': 39600,
            },
        ]
        for day_of_week in DAYS_OF_WEEK
    }
