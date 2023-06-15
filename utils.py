from datetime import datetime

def format_datetime(date_str, time_str):
    """Formats the date and time strings into a datetime object."""
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    time = datetime.strptime(time_str, "%H:%M").time()
    return datetime.combine(date, time)
