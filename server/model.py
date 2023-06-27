""" Models for the database """

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    """ User of the app """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)

    reservations = db.relationship("Reservation", back_populates="user")

class Reservation(db.Model):
    """ Reservation of the app """

    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    user = db.relationship("User", back_populates="reservations")


# Connects to book-melon database
def connect_to_db(flask_app, db_uri='postgresql:///book-melon', echo=True):
    """ Connects to the database """

    flask_app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    flask_app.config['SQLALCHEMY_ECHO'] = echo
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = flask_app
    db.init_app(flask_app)
    print('Connected to the db!')


if __name__ == '__main__':
    from server import app
    connect_to_db(app)