"""Parse request query params
"""


class QueryError(Exception):
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
    except KeyError:
        raise QueryError(
            'Missing query parameter: {parameter}'.\
            format(parameter=query_param))
