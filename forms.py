from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, TextField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.html5 import SearchField
from wtforms.validators import DataRequired, Length, InputRequired, Email, EqualTo

class SearchForm(FlaskForm):
    # [VARIABLE] = [FIELD TYPE]('[LABEL]', [validators=[VALIDATOR TYPE](message=('[ERROR MESSAGE'))])
    query = SearchField('Query', [DataRequired()])
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[('0', 'Worst'), ('1', 'Terrible'), ('2', 'Bad'), ('3', 'Average'), ('4', 'Good'), ('5', 'Excellent')])
    text = TextAreaField('Review', [DataRequired()])
    submit = SubmitField('Submit')

class SignupForm(FlaskForm):
    email = StringField('Email', [Length(min=6), Email(message="Not a valid email address."), DataRequired()])
    username = StringField('Username', [DataRequired()])
    password = PasswordField('Password', [Length(min=6, message="Select a stronger password."), DataRequired(message="Please enter a password.")])
    confirm = PasswordField('Confirm Your Password', [EqualTo("password", message="Password must match."), DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', [Email(message="Not a valid email address."), DataRequired()])
    password = PasswordField('Password', [DataRequired(message="Please enter a password.")])
    submit = SubmitField('Sign in')