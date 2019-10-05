from datetime import datetime

def datetime_to_str(dt_obj):
    """
    Takes a datetime object and returns a string representation of it.

    Example: 
    >>> from datetime import datetime
    >>> now = datetime.now()
    >>> now.strftime('%B %d, %Y)
    'September 30, 2019'
    """
    date_format = '%B %d, %Y'

    return dt_obj.strftime(date_format)
