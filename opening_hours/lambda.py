"""Format restaurant opening hours
"""

def handler(event, context):
    """Main API handler.

    Convert opening hours from request to human readable format
    """
    print('Im here')
    return {
        "statusCode": 200,
        "body": 'Hello world'
    }