# INF 601 - Advanced Python
# Illia Ivanov
# Mini Project 3

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email

class TaskForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=150)])
    description = TextAreaField("Description")
    category = SelectField("Category", coerce=int)
    is_done = BooleanField("Done?")
    submit = SubmitField("Save Task")

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")