# INF 601 - Advanced Python
# Illia Ivanov
# Mini Project 3

from app import create_app
from app.extensions import db
from app.models import Category

app = create_app()

with app.app_context():
    db.create_all()
    if not Category.query.first():
        db.session.add_all([
            Category(name="General"),
            Category(name="Study"),
            Category(name="Work"),
        ])
        db.session.commit()
        print("Database initialized and seeded.")
    else:
        print("Database already initialized.")
