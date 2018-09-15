"""Errors, related to request cleaning
"""
from src.exceptions import ValueErrorWithMessage


class CleanRequestError(ValueErrorWithMessage):
    """Error to be raised if cleaning request failed
    because of invalid format
    """
    pass
