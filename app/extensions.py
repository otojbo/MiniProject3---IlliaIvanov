# INF 601 - Advanced Python
# Illia Ivanov
# Mini Project 3

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "login"