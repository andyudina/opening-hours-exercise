"""Working shift.

Responsible for working shift creation from opening and closing working hours,
and printing shift in human readable format
"""
import json

from src.working_hours.exceptions import WorkingHoursError
from src.working_hours.utils import (
    is_closing_hour,
    is_opening_hour,
)
from src.utils import split_to_pairs


class Shift:
    """
    Restaurant working shift. Described by opening and closing hours.
    Opening and closing hours can be on the same day or on the subsequent days. Shift can be incomplete, i.e. either opening or closing hour is None.

    Attributes:
        open (int): UNIX time, that shows when shift starts
        close (int): UNIX time, that shows when restaurant ends
    """

    def __init__(self, open_hour, close_hour):
        """Return a Shift object, which start at *open_hour*
        and ends at *close_hour*
        """
        self.open = open_hour
        self.close = close_hour

    def need_closing_hour(self):
        """Check if current shift is incomplete and closing hour is missing
        """
        return self.open and not self.close

    def need_opening_hour(self):
        """Check if current shift is incomplete and opening hour is missing
        """
        return self.close and not self.open

    def to_dict(self):
        """Return dict, created from object fields
        """
        return self.__dict__

    @classmethod
    def create_shifts_from_json(cls, hours):
        """Create shifts from hours list

        Create shifts from pairs of opening and closing hours
        Separately return first closing hour and last opening hour if found
        Raise exception if pairs can not be found.

        Args:
            - hours (list): List with working hours
            Format:
            [
                {
                   'type': str, 'value': int
                }
            ]
            Type can be either 'close' or 'open'.
            Value is UNIX time

        Returns:
            - List of incomplete shifts - with only opening or closing hours
            - List of created shifts
        """
        # Check if first hour is unmatched closing hour
        # And create incomplete shifts
        incomplete_shifts = []
        if hours and is_closing_hour(hours[0]):
            # First hour type is closing.
            # Apparently previous day was not closed
            unmatched_closing_hour = hours[0]['value']
            incomplete_shifts.append(cls(None, unmatched_closing_hour))
            # Remove closing hours of previous day from list
            hours = hours[1:]
        if hours and is_opening_hour(hours[-1]):
            # Last hour type is closing. Apparently current day is not closed
            unmatched_opening_hour = hours[-1]['value']
            incomplete_shifts.append(cls(unmatched_opening_hour, None))
            # Remove closing hours of previous day from list
            hours = hours[:-1]
        # Process other hours
        opening_and_closing_hour_pairs = split_to_pairs(hours)
        shifts = list(map(
            lambda hour_pair: cls._try_convert_hours_pair_to_shift(hour_pair),
            opening_and_closing_hour_pairs))
        return incomplete_shifts, shifts

    @classmethod
    def _try_convert_hours_pair_to_shift(cls, hour_pair):
        """Validate that hours pairs has correct format and create shift

        Check if first hour in pair is opening, second one is closing and
        opening hour is before closing hour.
        Throw error if any of these conditions are not matched.

        Args:
            hours_pair (list): List of two elements with format:
            {
                'type': str, 'value': int
            }

        Returns:
            Shift with opening hour from first element of hour pair
            and with closing hour from second element of hour pair
        """
        # Raise error if pair size is invalid
        if len(hour_pair) != 2:
            raise WorkingHoursError(
                'Found unmatched hours. {}'.format(json.dumps(hour_pair)))
        # Process pair with valid size
        opening_hour, closing_hour = hour_pair
        if not is_opening_hour(opening_hour) or \
                not is_closing_hour(closing_hour) or \
                opening_hour['value'] > closing_hour['value']:
            raise WorkingHoursError(
                'Invalid opening and closing hours found. '
                'Opening hour should be before closing hour. '
                'Opening hour: {opening_hour}, Closing hour: {closing_hour}'.
                format(
                    opening_hour=opening_hour['value'],
                    closing_hour=closing_hour['value']))
        return cls(opening_hour['value'], closing_hour['value'])

    @classmethod
    def merge_shifts(cls, shift_with_opening_hour, shift_with_closing_hour):
        """Return new shift with opening hour from *shift_with_opening_hour*
        and closing hour from *shift_with_closing_hour*
        """
        return cls(
            shift_with_opening_hour.open,
            shift_with_closing_hour.close)
