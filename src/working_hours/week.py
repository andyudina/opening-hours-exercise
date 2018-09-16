"""Working week.

Responsible for week creation and printing in human readable format.
Group shifts that start on one day and end on another
"""
from first import first

from src.utils import filter_empty_keys
from src.working_hours.constants import WEEKDAYS
from src.working_hours.exceptions import WorkingHoursError
from src.working_hours.shift import Shift
from src.working_hours.utils import (
    get_or_throw_exception,
    get_next_day)
from src.working_hours.weekday import Weekday


class Week:
    """
    Restaurant working week. Consists of weekdays, which could be None

    Attributes:
        monday (working_hours.Weekday)
        tuesday (working_hours.Weekday)
        wednesday ((working_hours.Weekday)
        thursday (working_hours.Weekday)
        friday (working_hours.Weekday)
        saturday (working_hours.Weekday)
        sunday (working_hours.Weekday)
    """

    def __init__(self, **weekdays):
        """Return a Week object with weekdays from *weekdays*
        If some weekday was not passed, attribute will be set to None
        """
        for weekday in WEEKDAYS:
            setattr(
                self,
                weekday,
                weekdays.get(weekday, None)
            )

    def to_dict(self):
        """Return dict, created recursively from object fields
        """
        return [
            getattr(self, weekday).to_dict()
            for weekday in WEEKDAYS
            if getattr(self, weekday)
        ]

    def to_human_readable_format(self):
        """Return string with week working hours
        """
        return [
            getattr(self, weekday).to_human_readable_format()
            for weekday in WEEKDAYS
            if getattr(self, weekday)
        ]

    @classmethod
    def create_week_from_json(cls, working_hours_json):
        """Create week with all weekdays and shifts from working_hours dict

        Args:
            working_hours_json (dict): Dict with valid working hours
            Format:
            {
                'day_of_week': [
                    {
                       'type': str, 'value': int
                    }
                ]
            }

        Returns:
            Week object with weekdays and shifts
        """
        weekdays = {}
        weekdays_with_incomplete_shifts = {}
        for weekday_name in WEEKDAYS:
            weekday_hours = \
                get_or_throw_exception(weekday_name, working_hours_json)
            # Create weekday from json dict
            # Return separately closing or opening hours, which
            # Did not have pair during the same day
            incomplete_shifts, weekday = Weekday.create_weekday_from_json(
                weekday_name, weekday_hours)
            weekdays[weekday_name] = weekday
            weekdays_with_incomplete_shifts[weekday_name] = incomplete_shifts
        # Try match shifts that start at one day and end on the next day
        cls._match_unmatched_hours(
            weekdays, weekdays_with_incomplete_shifts)
        return cls(**weekdays)

    @classmethod
    def _match_unmatched_hours(cls, weekdays, weekdays_with_incomplete_shifts):
        """Try create shifts for unmatched hours.

        Appends shifts for weekday in place.

        Args:
            - weekdays (dict): Dict of weekdays. Keys are weekday names.
            Values are working_hours.Weekday objects
            - weekdays_with_incomplete_shifts (dict): Dict of weekdays.
            Keys are weekday names and values are incomplete shifts
            Values can be None
        """
        # Split shifts into to dicts:
        # for shifts with opening hour and for shifts with closing hour
        # Create dict for shifts with open hours
        shifts_with_opening_hour = {
            weekday: first(
                [shift for shift in shifts if shift.need_closing_hour()]
            )
            for weekday, shifts in weekdays_with_incomplete_shifts.items()
        }
        shifts_with_opening_hour = filter_empty_keys(shifts_with_opening_hour)
        # Create dict for shifts with close hour
        shifts_with_closing_hour = {
            weekday: first(
                [shift for shift in shifts if shift.need_opening_hour()]
            )
            for weekday, shifts in weekdays_with_incomplete_shifts.items()
        }
        shifts_with_closing_hour = filter_empty_keys(shifts_with_closing_hour)
        # Try find closing hour for opening hour
        for weekday_name, shift in shifts_with_opening_hour.items():
            if not shift:
                continue
            # Find shift with closing hours
            # for current shift with opening hours
            next_day_name, next_day_shift = \
                get_next_day(weekday_name, shifts_with_closing_hour)
            if not next_day_shift:
                raise WorkingHoursError(
                    'Found opening hours without corresponding closing hours')
            # Create merged shift and add it to weekday, on which shift started
            merged_shift = Shift.merge_shifts(shift, next_day_shift)
            weekdays[weekday_name].add_shift(merged_shift)
            # Remove shift with closing hours from a dict
            shifts_with_closing_hour.pop(next_day_name, None)
        # Raise error if any of closing hours were left unmatched
        if shifts_with_closing_hour:
            raise WorkingHoursError(
                'Found closing hours without corresponding opening hours')
