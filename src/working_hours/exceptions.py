"""Errors, related to working hours processing
"""
from src.exceptions import ValueErrorWithMessage


class WorkingHoursError(ValueErrorWithMessage):
    """Error to be raised if working hours can not be created
    or printed in human readable format because of invalid input
    """
    pass
