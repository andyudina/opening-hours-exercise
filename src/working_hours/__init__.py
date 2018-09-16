"""Encapsulates working hours related logic:
- Create working shifts by grouping working hours in pairs
- Create week and weekdays
- Create working shifts using working hours from different day
- Print working hour in human readable format
"""
from src.working_hours.exceptions import WorkingHoursError
from src.working_hours.shift import Shift
from src.working_hours.week import Week
from src.working_hours.weekday import Weekday
