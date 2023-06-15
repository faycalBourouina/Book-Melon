from flask import Flask, request, render_template, session
import model
import crud
import os
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
def user_booking(username, resevation):
    """ Add a reservation to the user's reseravation"""

    reservation = request.form.get("reservation")
    return f"Reservation {reservation} added to {username}'s resrvations"


if __name__ == '__main__':
        app.run(host="0.0.0.0", debug=True)