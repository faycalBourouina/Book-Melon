from flask import Flask, request, render_template, session, jsonify
import model
import crud
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)

# connect to the database and create tables
model.connect_to_db(app)
with app.app_context():
    model.db.create_all()


# Load the API key from the .env file
load_dotenv()

# session secret key
app.secret_key = os.getenv("SESSION_SECRET_KEY")



@app.route("/")
def hello():
    """ Displays the homepage"""
    return render_template("index.html")

@app.route("/landing")
def get_landing_page():
    """ Displays the landing page"""

    # If user is logged in, display the reservation page
    if session.get("username"):
        username = session["username"]
        reservations = crud.get_reservation_page(username)
        response  = jsonify({"reservations": reservations})
        return response
    # Don't display the reservation page
    else:
        return "Please log in to view your reservations"

@app.route("/signup", methods=["POST"])
def signup():
    """ Creates a new user """

    username = request.form.get("username")
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

    username = request.form.get("username")

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

@app.route("/<username>/reservations")
def user_bookings(username):
    """ Displays the user's reservations """
    print("username in session", session["username"])
    
    return f"Bookings for {username}"

@app.route("/<username>/reservation/<reservation>", methods=["POST"])
def add_reservation(username, resevation):
    """ Add a reservation to the user's reseravation"""

    # Retrieve the request data
    data = request.json
    reservation_date = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    # Add the reservation using the CRUD function
    reservation = crud.add_reservation(username, reservation_date, start_time, end_time)


if __name__ == '__main__':
        app.run(host="0.0.0.0", debug=True)