from flask import (Flask, request, render_template, session, jsonify)
from utils import sqlalchemy_obj_to_dict
import model
import crud
import os
import json
from flask_cors import CORS
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# connect to the database and create tables
model.connect_to_db(app)
with app.app_context():
    model.db.create_all()


# Load the API key from the .env file
load_dotenv()

# session secret key
app.secret_key = os.getenv("SESSION_SECRET_KEY")


@app.route("/")
def get_landing_page():
    """ Displays the landing page"""

    username = request.args.get("username")

    # If user is logged in, display the reservation page
    if "username" in session:
        username = session["username"]
        reservations = crud.get_reservation_page(username)
        reservations_dict = [sqlalchemy_obj_to_dict(reservation) for reservation in reservations]
        response  = jsonify({"reservations": reservations_dict})
        return response, 200
    # Don't display the reservation page
    else:
        response = jsonify({"message": "User not logged in"})
        return response, 401

@app.route("/signup", methods=["POST"])
def signup():
    """ Creates a new user """

    username = request.json.get("username")
    new_user = crud.create_user(username)
    # if the user doesn't already exist, add them to the database
    if new_user:
        session["username"] = username
        model.db.session.add(new_user)
        model.db.session.commit()
        return f"User {username} created"
    else:
        return f"User {username} already exists"


@app.route("/login", methods=["POST"])
def login():
    """ Logs in the user """

    username = request.json.get("username")
    print("username", username)
    existing_user = crud.authenticate_user(username)
    if existing_user:
        session["username"] = username
        return f"User {username} logged in"
    else:
        return f"User {username} does not exist"

@app.route("/logout")
def logout():
    """ Logs out the user """

    session.pop("username")
    return "user logged out"

@app.route("/reservations")
def user_bookings():
    """ Displays the user's reservations """
    if "username" in session:
        username = session["username"]
        reservations = crud.get_reservation_page(username)
        reservations_dict = [sqlalchemy_obj_to_dict(reservation) for reservation in reservations]
        response = jsonify({"reservations": reservations_dict})
        return response, 200
    else:
        response = jsonify({"message": "User not logged in"})
        return response, 401

@app.route("/reservations/reservation", methods=["POST"])
def add_reservation():
    """ Add a reservation to the user's reseravation"""

    # Retrieve the request data
    date = request.json.get("date")
    start_time = request.json.get("start_time")
    end_time = request.json.get("end_time")

    print("booking: ", date, start_time, end_time)

    username = session["username"]
    # Add the reservation using the CRUD function
    reservation = crud.add_reservation(username, date, start_time, end_time)

    if reservation == "reservation_exists":
        return jsonify({"message": "Reservation already exists"})
    elif reservation == "user_reservation_exists":
        return jsonify({"message": "User already has a reservation on this date"})
    
    model.db.session.add(reservation)
    model.db.session.commit()
    reservation_dict = sqlalchemy_obj_to_dict(reservation)
    response = jsonify({"resrvation": reservation_dict})
    return response


if __name__ == '__main__':
        app.run(debug=True, port=8080)