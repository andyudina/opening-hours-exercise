"""Custom base error class
"""


class ValueErrorWithMessage(ValueError):
    """Custom ValueError with message attribute
    """

    def __init__(self, message, *args, **kwargs):
        super(ValueErrorWithMessage, self).__init__(message, *args, **kwargs)
        self.message = message
