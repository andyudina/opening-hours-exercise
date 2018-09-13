"""Clean opening hours 
"""

class CleanRequestError(Exception):
    """Error to be raised if cleaning request failed
    because of invalid format
    """
    pass

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
                        'open': time obj,
                        'close': time obj
                    }
                ],
                'is_open': boolean
            }
        ]
    """