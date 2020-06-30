import requests
from flask import Flask, render_template, request

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://tuvu:123456@localhost:5432/app"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Tie database to this app
# db.init_app(app)

# API key required for authentication
api_key="2f0dbac34c4d747c83895d65efad8073"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    return render_template("search.html")

@app.route("/search/movies", methods=["POST"])
def movies():
    global api_key
    # Retrieve input from users
    title = request.form.get("title")

    # GET list of movies with related title
    res = requests.get("https://api.themoviedb.org/3/search/movie?", params={"api_key": api_key, "query": title})

    # Make sure request works
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")

    # Convert response into nice json format
    results = res.json()['results']

    # Redirect users to a new html page
    return render_template("movies.html", results=results)

@app.route("/search/movies/<int:movie_id>/<string:movie_title>")
def movie(movie_id, movie_title):
    global api_key
    
    # GET movie's details with its id 
    res = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id), params={"api_key": api_key})

    # Make sure request works
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful." + str(res.status_code))

    # Convert response into nice json format
    movie_info = res.json()

    # Redirect users to a new html page
    return render_template("movie.html", movie_info=movie_info)