from flask_wtf import FlaskForm
from wtforms import StringField, TextField, SubmitField, PasswordField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired, Length, InputRequired, Email, EqualTo

class SearchForm(FlaskForm):
    # [VARIABLE] = [FIELD TYPE]('[LABEL]', [validators=[VALIDATOR TYPE](message=('[ERROR MESSAGE'))])
    query = SearchField('Query', [DataRequired()])
    submit = SubmitField('Search')

class SignupForm(FlaskForm):
    email = StringField('Email', [Length(min=6), Email(message="Not a valid email address."), DataRequired()])
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [Length(min=6, message="Select a stronger password."), DataRequired(message="Please enter a password.")])
    confirm = PasswordField('Confirm Your Password', [EqualTo("password", message="Password must match."), DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', [Email(message="Not a valid email address."), DataRequired()])
    password = PasswordField('Password', [DataRequired(message="Please enter a password.")])
    submit = SubmitField('Login')