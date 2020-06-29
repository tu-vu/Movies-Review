import requests
from flask import Flask, render_template, request

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://tuvu:123456@localhost:5432/app"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Tie database to this app
# db.init_app(app)

api_key="2f0dbac34c4d747c83895d65efad8073"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    return render_template("login.html", email=email, password=password)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search/movies", methods=["POST"])
def movies():
    global api_key
    title = request.form.get("title")
    res = requests.get("https://api.themoviedb.org/3/search/movie?", params={"api_key": api_key, "query": title})
    result = None
    if res.status_code == 200:
        results = res.json()['results']
    return render_template("movies.html", results=results)
    
