############################ SET UP ############################
from flask import Flask, url_for, render_template, request, redirect, flash
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from config import Config
import requests

# Import all models
from forms import *
from models import *

# Global accessible libraries

app = Flask(__name__)
app.config.from_object(Config)

login_manager = LoginManager()
login_manager.init_app(app)

# Tie database to this app
db.init_app(app)