from datetime import datetime, time, date

def sqlalchemy_obj_to_dict(obj):
    """Convert a SQLAlchemy object to a dictionary."""

    obj_dict = {}
    for column in obj.__table__.columns:
        value = getattr(obj, column.name)
        if isinstance(value, date):
            value = value.isoformat()
        elif isinstance(value, time):
            value = value.strftime("%H:%M:%S")
        obj_dict[column.name] = value
        
    return obj_dict

def format_date(date_str):
    """Formats the date string into a datetime object."""
    date = datetime.strptime(date_str, "%m/%d/%Y").date()
    return date

def format_time(time_str):
    """Formats the time string into a datetime object."""
    time = datetime.strptime(time_str, "%H:%M").time()
    return time