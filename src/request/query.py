"""Parse request query params
"""
from src.exceptions import ValueErrorWithMessage


class QueryError(ValueErrorWithMessage):
    """Error to be raised if parsing query params failed
    """
    pass


def get_query_param(request, query_param):
    """Get query parameter value from request

    Raises QueryError if parameter is missing
    Raises KeyError if request format is invalid

    Args:
        request (dict)
        query_param (str): Parameter name

    Returns:
        Query parameter value
    """
    query_string_params = request['queryStringParameters']
    try:
        return query_string_params[query_param]
    except (KeyError, TypeError):
        raise QueryError(
            'Query parameter "{parameter}" is missing'.
            format(parameter=query_param))
