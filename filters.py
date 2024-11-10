from datetime import datetime, date

def format_date(value):
    """Format a date to 'dd-mm-yyyy'."""
    if isinstance(value, (datetime, date)):
        return value.strftime('%d-%m-%Y')
    return value
