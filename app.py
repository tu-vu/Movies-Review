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

############################ ROUTES ############################
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
            # next_page = request.args.get('next') # Get recent page users trying to view
            # return redirect(next_page or url_for('search'))
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
                user = User(username=form.username.data, email=form.email.data, password=form.password.data)
                db.session.add(user)
                db.session.commit() # Create new user
                login_user(user) # Log in as newly created user - magically!
                # Go to movie search page
                return redirect(url_for('search'))
            flash("Username already exists!")
        else:
            flash("A user already exists with that email address.")
    return render_template("signup.html", form=form)

@app.route("/search")
@login_required
def search():
    # TODO: Learn about form validation using WTForm 
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('movies'))
    return render_template("search.html", form=form)

@app.route("/search/movies", methods=["POST"])
@login_required
def movies():
    global API_KEY
    # Retrieve input from users
    title = request.form.get("title")

    # GET list of movies with related title
    res = requests.get("https://api.themoviedb.org/3/search/movie?", params={"api_key": API_KEY, "query": title})

    # Make sure request works
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    # Convert response into nice json format
    results = res.json()['results']

    # Redirect users to a new html page
    return render_template("movies.html", results=results)

@app.route("/search/movies/<int:movie_id>/<string:movie_title>", methods=["GET","POST"])
@login_required
def movie(movie_id, movie_title):
    global API_KEY
    
    # GET movie's details with its id 
    res = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id), params={"api_key": API_KEY})

    # Make sure request works
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful." + str(res.status_code))

    # Convert response into nice json format
    movie_info = res.json()

    # Redirect users to a new html page
    return render_template("movie.html", movie_info=movie_info)

# Given *user_id*, return the associated User object
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