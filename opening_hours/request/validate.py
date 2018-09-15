"""Validate request schema
"""
from jsonschema import (
    validate,
    # ValidationError should be imported from request.validate module
    ValidationError
)

from opening_hours.constants import DAYS_OF_WEEK


# JSON schema for working hours request

ONE_DAY_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "type": {
                "type": "string",
                "enum": ["open", "close"]
            },
            "value": {
                "type": "number",
                "minimum": 0,
                "maximum": 86399, # Max value for working hour (11.59:59 PM)
                "exclusiveMaximum": False
            },
        },
        "required": ["type", "value"]
    }
}

WORKING_HOURS_SCHEMA = {
    "type": "object",
    "properties": {
        day_of_week: ONE_DAY_SCHEMA
        for day_of_week in DAYS_OF_WEEK
    },
    "required": DAYS_OF_WEEK
}

def validate_request(request):
    """Validate request using jsonschema

    Raises ValidationError if request is invalid
    """
    validate(request, WORKING_HOURS_SCHEMA)
