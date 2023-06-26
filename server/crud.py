from model import User, Reservation, db
from utils import format_date, format_time

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


def add_reservation(username, date, start_time, end_time):
    """Add a reservation to the user's reservations."""
    
    # Format the date and time strings into datetime objects
    date = format_date(date)
    start_time = format_time(start_time)
    end_time = format_time(end_time)

 # Check if any reservation exists on the specified date and time range
    existing_reservation = Reservation.query.filter(
        Reservation.date == date,
        Reservation.start_date == start_time,
    ).first()

    if existing_reservation:
        return "reservation_exists"

    # Find the user
    user = User.query.filter_by(username=username).first()

    # Check if the user already has a reservation on the specified date
    existing_user_reservation = Reservation.query.filter_by(
        user_id=user.id, date=date
    ).first()


    if existing_user_reservation:
        return "user_reservation_exists"

    # Create a new reservation
    reservation = Reservation(
        user_id=user.id,
        date=date,
        start_date=start_time,
        end_date=end_time,
    )

    return reservation