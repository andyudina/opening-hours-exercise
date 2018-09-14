"""Decode query from base64 format and parse json
"""
import base64
import binascii
import json


class ParseError(Exception):
    """Error to be raised if parsing request failed
    """
    pass

def decode_and_load_json(query):
    """Decode query from base64

    Throws ParseError if base64 or json is invalid 

    Args:
        query (str): json request decoded as base64

    Returns:
        Decoded and parsed JSON request
    """
    try:
        decoded_query = base64.b64decode(query)
    except binascii.Error:
        raise ParseError('Invalid base64 format')
    try:
        return json.loads(decoded_query)
    except json.JSONDecodeError:
        raise ParseError('Invalid json format')
