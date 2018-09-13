"""Clean opening hours 
"""
from opening_hours.constants import DAYS_OF_WEEK_WITH_ORDER
from opening_hours.utils import split_to_pairs


class CleanRequestError(Exception):
    """Error to be raised if cleaning request failed
    because of invalid format
    """
    pass

def _sort_by_day_of_week(opening_hours):
    """Sort opening hours according to day of week - from Monday to Sunday

    Args:
        opening_hours (list): List of lists, representing opening hours.
            First element of every internal list is expected to be day of week.
            For example: monday, tuesday, wednesday etc.

    Returns:
        Same list of opening hours sorted by day of week
    """
    return sorted(
        opening_hours, 
        key=lambda dow: DAYS_OF_WEEK_WITH_ORDER.get(dow[0]))

def _is_closing_hour(hour):
    """Validate if hour is closing

    Args:
        hour (dict): Opening or closing hour with type an value. Format:
            {
                'type': str, 'value': int
            }

    Returns:
        Boolean flag, that shows if hour is closing
    """
    return hour['type'] == 'close'

def _is_opening_hour(hour):
    """Validate if hour is open

    Args:
        hour (dict): Opening or closing hour with type an value. Format:
            {
                'type': str, 'value': int
            }

    Returns:
        Boolean flag, that shows if hour is closing
    """
    return hour['type'] == 'open'

def _process_one_day(day_of_week, opening_hours):
    """Transform opening hours of one day to simplified format

    Args:
        day_of_week (str): Name of processed day
        opening_hours (list): List of opening hours. Format:
            [
                {
                    'type': str, 'value': int
                }
            ]

    Returns:
        prev_day_closing_hour (int): Closing hours for previous day if found.
            Can be None.
        current_day (dict): Current day and its opening hours. Format:
            {
                'day_of_week': str,
                'opening_hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ],
                'is_open': boolean
            }
    """
    current_day = {
        'day_of_week': day_of_week
    }
    if not opening_hours:
        # Restaurant is closed all day
        return None, \
            {
                'opening_hours': [],
                'is_open': False,
                **current_day
            }
    # Process hours for the previous day shifts
    prev_day_closing_hour = None
    if _is_closing_hour(opening_hours[0]):
        # First hour type is closing. Apparently previous day was not closed
        prev_day_closing_hour = opening_hours[0]['value']
        # Remove closing hours of previous day from list
        opening_hours = opening_hours[1:]
    # Process hours for the current day shifts
    opening_and_closing_hours_pairs = split_to_pairs(opening_hours)
    result_hours = []
    for pair in opening_and_closing_hours_pairs:
        if len(pair) == 1:
            if _is_opening_hour(pair[0]):
                # Only opening hours without pair is possible
                # This means that restaurant will be closed on the next day
                result_hours.append(
                    {
                        'open': pair[0]['value'],
                    }
                )
                # Only last pair can consist of one value
                break
            else:
                raise CleanRequestError(
                    'Invalid hour found. '
                    'Only opening hour can be without pair on the same day'
                    'Day of week: %s. Time: %d' % (
                        day_of_week, pair[0]['value']))
        opening_hour, closing_hour = pair
        if not _is_opening_hour(opening_hour) or \
                not _is_closing_hour(closing_hour) or \
                opening_hour['value'] > closing_hour['value']:
            # Expect opening hour to be before closing hour
            raise CleanRequestError(
                'Invalid opening and closing hours found. '
                'Opening hour should be before closing hour. '
                'Day of week: %s. Opening hour: %d, Closing hour: %d' % (
                    day_of_week, opening_hour['value'], closing_hour['value']))
        result_hours.append(
            {
                'open': opening_hour['value'],
                'close': closing_hour['value']
            }
        )
    return prev_day_closing_hour, \
        {
            'opening_hours': result_hours,
            'is_open': len(result_hours) > 0,
            **current_day
        }

def _is_last_day_incomplete(processed_days):
    """Validate if last day of already processed days doesn't have closing time

    Args:
        processed_days (list): List of already processed days

    Returns:
        Boolean flag, that shows if last day is incomplete
    """
    if not processed_days:
        # No processed days
        return False
    last_day = processed_days[-1]
    if not last_day['opening_hours']:
        # During last day restaurant was closed 
        return False
    # Last shift shouldn't have closing hours
    return last_day['opening_hours'][-1].get('close', None) is None

def _complete_last_day(prev_day, prev_day_closing_hour):
    """Add closing hours from prev_day_diff to last shift of prev_day

    Args:
        prev_day (dict): Processed opening hours for one day. Format:
            {
                'day_of_week': str,
                'opening_hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ],
                'is_open': boolean
            }
        prev_day_closing_hour (int): Missing closing time o last shift

    Returns:
        Updated previous day with completed closing time
    """
    prev_day['opening_hours'][-1].\
        update({ 'close': prev_day_closing_hour })
    return prev_day

def clean(opening_hours_request):
    """Transform JSON request with opening hours to simplify further processing

    Args:
       opening_hours_request (dict): Valid dictionary with opening hours:
       Format:
       { 
            'day_of_week(string)': [
                {
                    'type': str, 'value': int
                }
            ] 
        }

    Returns:
        List of opening hours by days. Format:
        [
            {
                'day_of_week': str,
                'opening_hours': [
                    {
                        'open': int,
                        'close': int
                    }
                ],
                'is_open': boolean
            }
        ]
    """
    result_hours = []
    for day_of_week, opening_hours in \
            _sort_by_day_of_week(opening_hours_request.items()):
        prev_day_closing_hour, current_day = \
            _process_one_day(day_of_week, opening_hours)
        # Try complete previous day
        # If restaurant is not closed during the same day
        if prev_day_closing_hour is not None:
            if _is_last_day_incomplete(result_hours):
                # Add missing closing hours for
                completed_last_day = _complete_last_day(
                    result_hours[-1], prev_day_closing_hour)
                result_hours = result_hours[:-1] + [completed_last_day]
            else:
                # Throw error if day starts with closing hours
                # But the previous day closing hours were already processed
                raise CleanRequestError(
                    'Close hours found without corresponding opening hours. '
                    'Day of week: %s. Time: %d' % (
                        day_of_week, prev_day_closing_hour))
        if _is_last_day_incomplete(result_hours):
            # Last day is incomplete, but current day doesn't have
            # missing closing hours
            raise CleanRequestError(
                'Opening hours found without corresponding closing hours. '
                'Day of week: %s. Time: %d' % (
                    result_hours[-1]['day_of_week'],
                    result_hours[-1]['opening_hours'][-1]['open']))
        # Add current date to result
        result_hours.append(current_day)
    # Check if last day in week is incomplete
    if _is_last_day_incomplete(result_hours):
        # Last day is incomplete, but current day doesn't have
        # missing closing hours
        raise CleanRequestError(
            'Opening hours found without corresponding closing hours. '
            'Day of week: %s. Time: %d' % (
                result_hours[-1]['day_of_week'],
                result_hours[-1]['opening_hours'][-1]['open']))
    return result_hours
