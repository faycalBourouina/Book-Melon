from flask import Flask, request, render_template, session
import model
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


@app.route("/login", methods=["POST"])
def login():
    """ Logs in the user """

    username = request.form.get("username")
    session["username"] = username
    print("username in session", session["username"])
    return f"user {username} logged in"

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