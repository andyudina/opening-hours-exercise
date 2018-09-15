"""Weekdays names and order numbers
"""

WEEKDAYS = [
    'monday', 'tuesday', 'wednesday',
    'thursday', 'friday', 'saturday', 'sunday'
]

WEEKDAYS_WITH_ORDER = {
    name: index
    for index, name in enumerate(WEEKDAYS)
}
