from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "users"
    # an easy way to reference each user
    id = db.Column(db.Integer, primary_key=True)

    # Duplicate emails/usernames are not allowed
    # nullable = False -> can't be blank
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Declare a relationship between User and Review
    # backref = users allows Review to refer back to user, e.g my_review.user
    # lazy = True means we will only load data when it's accessed
    reviews = db.relationship("Review", backref="user",lazy=True)

    def add_review(self, rating, text):
        review = Review(rating=rating, text=text, author=self.username)
        db.session.add(review)
        db.session.commit()

    def __repr__(self):
        return "<User {}>".format(self.username)

class Review(db.Model):
    __tablename__ = "reviews"
    # an easy way to reference each review
    id = db.Column(db.Integer, primary_key=True)

    # Which movie to be reviewd
    movie = db.Column(db.String, nullable=False)

    # Rating review (on a scale from 1-5, 5 being excellent, 1 being worst etc)
    rating = db.Column(db.Integer, nullable=False)

    # Typed review from users
    text = db.Column(db.String, nullable=False)

    # Name of reviewer
    author = db.Column(db.String, db.ForeignKey('users.username') , nullable=False)

    # Time when the review was made
    # No need to worry about this since we already default it to "now"
    timestamp = db.Column(db.DateTime(), default=datetime.utcnow, index=True)