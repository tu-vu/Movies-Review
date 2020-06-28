from flask import Flask, render_template, request

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://tuvu:123456@localhost:5432/app"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Tie database to this app
#db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    return render_template("login.html", username=username, password=password)
