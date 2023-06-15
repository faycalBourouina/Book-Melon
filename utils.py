from datetime import datetime

def format_date(date_str):
    """Formats the date string into a datetime object."""
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    return date

def format_time(time_str):
    """Formats the time string into a datetime object."""
    time = datetime.strptime(time_str, "%H:%M").time()
    return time