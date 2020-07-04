############################ SET UP ############################
from flask import Flask, url_for, render_template, request, redirect, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from config import Config
import requests

# Import all models
from forms import *
from models import *

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

# Tie database to this app
db.init_app(app)

# Create all tables in local database
with app.app_context():
    db.create_all()

############################ AUTHENTICATION ############################
# Given *user_id*, return the associated User object. 
# Also, we can access current user info via current_user.attribute
@login_manager.user_loader
def load_user(user_id):
    """ Check if user is logged-in on every page load. """
    if user_id:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    """ Redirect unauthorized users to Login page. """
    flash("You must be logged in to view that page")
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
def login():
    """
    Log-in page for registered users
    GET requests serve log-in page.
    POST requests validate and redirect user to search page
    """
    # Bypass if user is already logged in 
    if current_user.is_authenticated:
        return redirect(url_for('search'))

    form = LoginForm()
    # Validate login attempt
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # If user exists in our database and password matches
        if user and user.password == form.password.data:
            login_user(user) # Log in as existing user
            return redirect(url_for('search'))
        elif not user:
            flash("Account does not exists!")
        else:
            flash("Password does not match!")
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    ### User log-out logic. ###
    logout_user()
    return redirect(url_for('login'))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    User sign-up page.
    GET requests serve sign-up page.
    POST requests validate form & user creation.
    """
    form = SignupForm()
    if form.validate_on_submit():
        # Users fill form correctly
        # Check if email already exists
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            # Check if username already exists
            existing_username = User.query.filter_by(username=form.username.data).first()
            if existing_username is None:
                user = User(username=form.username.data, 
                            email=form.email.data, 
                            password=form.password.data)
                db.session.add(user)
                db.session.commit() # Create new user
                login_user(user) # Log in as newly created user - magically!
                # Go to movie search page
                return redirect(url_for('search'))
            flash("Username already exists!")
        else:
            flash("A user already exists with that email address.")
    return render_template("signup.html", form=form)

############################ ROUTES ############################
@app.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        # Redirect user to page that displays relevant movies based on user query
        return redirect(url_for('movies', query=form.query.data))
    return render_template("search.html", form=form)

@app.route("/search/movies")
@login_required
def movies():
    query = request.args.get("query")

    # GET list of related movies
    res = requests.get("https://api.themoviedb.org/3/search/movie?", params={"api_key": Config.API_KEY, "query": query})

    # Make sure request works
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    # Convert response into nice json format
    results = res.json()['results']

    # Register movies page view to user
    return render_template("movies.html", results=results)

@app.route("/search/movies/<string:movie_title>", methods=["GET","POST"])
@login_required
def movie(movie_title):
    form = ReviewForm()

    movie_id = request.args.get("movie_id")

    # GET movie's details with its id 
    res = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id), params={"api_key": Config.API_KEY})

    # Make sure request works
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful." + str(res.status_code))

    # Convert response into nice json format
    movie_info = res.json()

    # Check if user is accessing page via POST request
    if form.validate_on_submit(): 
        # Add user's review to database
        current_user.add_review(movie_title=movie_info['title'], rating=form.rating.data, text=form.text.data)

        # Redirect user to current page instead of directly render_template (which might results in duplicate POST requests!)
        return redirect(url_for('movie', form=form, movie_title=movie_title, movie_id=movie_id))

    # Get list of reviews for current movie
    reviews = Review.query.filter_by(movie_title=movie_title).all()

    # Register movie info view for users
    return render_template("movie.html", form=form, movie_info=movie_info, reviews=reviews) 