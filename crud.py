from mode import User, Reservation
from utils import format_datetime

def create_user(username):
    """ Create and return a new user """
    # Verify that the user doesn't already exist
    if User.query.filter_by(username=username).first():
        return None
    else:
        new_user = User(username=username)
        return new_user
    

def authenticate_user(username):
    """ Authenticate the user """

    # Verify that the user exists
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    else:
        return None


def get_reservation_page(username):
    """ Get the reservation page for the user """

    #get the user id from the username
    user_id = User.query.filter_by(username=username).first().id

    # get all the reservations for the user
    reservations = Reservation.query.filter_by(user_id=user_id).all()

    return reservations


def add_reservation(username, reservation_date, start_time, end_time):
    """Add a reservation to the user's reservations."""
    
    # Format the date and time strings into datetime objects
    reservation_date = format_datetime(reservation_date, start_time)
    start_time = format_datetime(reservation_date, start_time)
    end_time = format_datetime(reservation_date, end_time)

 # Check if any reservation exists on the specified date and time range
    existing_reservation = Reservation.query.filter(
        Reservation.date == reservation_date,
        Reservation.start_date <= start_time,
        Reservation.end_date >= end_time
    ).first()

    if existing_reservation:
        return None

    # Find the user
    user = User.query.filter_by(username=username).first()


    # Create a new reservation
    reservation = Reservation(
        user_id=user.id,
        date=reservation_date,
        start_date=start_time,
        end_date=end_time,
    )

    return reservation