"""Working day.

Represents weekday with corresponding shifts
Responsible fr printing information in human readable format
"""
from src.working_hours.shift import Shift


class Weekday:
    """
    Restaurant working day. Described by weekday name and shifts.
    Restaurant can be closed during whole day

    Attributes:
        name (str): Weekday name
        shifts (list): List of working_hour.Shift objects
    """

    def __init__(self, name, shifts):
        """Return a Weekday object with day_of_week name *name*
        and shifts list *shifts*
        """
        self.name = name
        self.shifts = shifts or []

    @property
    def is_closed(self):
        """Returns flag to show if restaurant is close during this weekday
        """
        return not self.shifts

    def add_shift(self, shift):
        """Append shift to own shifts list
        """
        self.shifts.append(shift)

    def to_dict(self):
        """Return dict, created recursively from object fields and properties
        """
        return {
            'day_of_week': self.name,
            'hours': [
                shift.to_dict() for shift in self.shifts
            ],
            'is_open': not self.is_closed,
        }

    def to_human_readable_format(self):
        """Return string with weekday working hours in human-readable format.
        For example: "Monday: 8 AM - 1 PM, 6 PM - 1 PM"
        """
        shifts = self._get_shifts_in_human_readable_format()
        return '{day_of_week}: {shifts}'.format(
            day_of_week=self.name.capitalize(),
            shifts=shifts)

    def _get_shifts_in_human_readable_format(self):
        """Return string with current weekday shifts in human-readable format.
        For example: "8 AM - 1 PM, 6 PM - 1 PM"
        """
        if self.is_closed:
            return 'Closed'
        return ', '.join(
            [
                shift.to_human_readable_format()
                for shift in self.shifts
            ]
        )

    @classmethod
    def create_weekday_from_json(cls, weekday_name, weekday_hours):
        """Create weekday with name as *weekday_name* and shifts, created from
        *weekday_shifts*

        Create shifts from pairs of opening and closing hours
        from *weekday_shifts*. Hours without pair are returned separately.

        Args:
            - weekday_name (str)
            - weekday_hours (list): List with working hours
            Format:
            [
                {
                   'type': str, 'value': int
                }
            ]

        Returns:
            - List of incomplete shifts (can be empty)
            - Weekday object with shifts
        """
        incomplete_shifts, shifts = \
            Shift.create_shifts_from_json(weekday_hours)
        return incomplete_shifts, cls(weekday_name, shifts)
