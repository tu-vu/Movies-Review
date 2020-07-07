""" Routes for page content """
from flask import Blueprint, url_for, render_template, request, redirect, flash
from flask_login import current_user, login_required
from .forms import SearchForm, ReviewForm
from .models import Review
from .import Config
import requests

# Blueprint Configuration
main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route("/search", methods=["GET", "POST"])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        # Redirect user to page that displays relevant movies based on user query
        return redirect(url_for('main_bp.movies', query=form.query.data))
    return render_template("search.html", form=form)

@main_bp.route("/search/movies", methods=["GET"])
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

@main_bp.route("/search/movies/<string:movie_title>", methods=["GET","POST"])
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
        return redirect(url_for('main_bp.movie', form=form, movie_title=movie_title, movie_id=movie_id))

    # Get list of reviews for current movie
    reviews = Review.query.filter_by(movie_title=movie_title).all()

    # Register movie info view for users
    return render_template("movie.html", form=form, movie_info=movie_info, reviews=reviews) 