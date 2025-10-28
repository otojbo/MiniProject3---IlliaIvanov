# INF 601 - Advanced Python
# Illia Ivanov
# Mini Project 3


from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import TaskForm, RegisterForm, LoginForm
from app.extensions import db, login_manager
from app.models import Task, Category, User
from sqlalchemy import or_


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key-change-me"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskboard.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id: str):
        return User.query.get(int(user_id))

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/tasks", methods=["GET", "POST"])
    @login_required
    def tasks():
        form = TaskForm()
        categories = Category.query.order_by(Category.name).all()
        form.category.choices = [(0, "— No category —")] + [(c.id, c.name) for c in categories]

        if form.validate_on_submit():
            category_id = form.category.data or 0
            category_id = None if category_id == 0 else category_id
            t = Task(
                title=form.title.data,
                description=form.description.data,
                is_done=form.is_done.data,
                user_id=current_user.id,
                category_id=category_id,
            )
            db.session.add(t)
            db.session.commit()
            flash("Task created.", "success")
            return redirect(url_for("tasks"))

        all_tasks = (
            Task.query.filter_by(user_id=current_user.id)
            .order_by(Task.created_at.desc())
            .all()
        )
        return render_template("tasks.html", form=form, tasks=all_tasks)

    @app.route("/tasks/<int:task_id>/toggle", methods=["POST"])
    @login_required
    def toggle_task(task_id: int):
        t = Task.query.filter_by(id=task_id, user_id=current_user.id).first()
        if not t:
            flash("Task not found.", "danger")
            return redirect(url_for("tasks"))
        t.is_done = not t.is_done
        db.session.commit()
        return redirect(url_for("tasks"))

    @app.route("/categories", methods=["GET", "POST"])
    @login_required
    def categories():
        if request.method == "POST":
            name = (request.form.get("name") or "").strip()
            if not name:
                flash("Category name cannot be empty.", "danger")
            elif Category.query.filter_by(name=name).first():
                flash("Category already exists.", "warning")
            else:
                db.session.add(Category(name=name))
                db.session.commit()
                flash("Category added.", "success")
            return redirect(url_for("categories"))

        cats = Category.query.order_by(Category.name).all()
        return render_template("categories.html", categories=cats)

    @app.route("/profile")
    @login_required
    def profile():
        return render_template("profile.html")

    @app.route("/auth/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = RegisterForm()
        if form.validate_on_submit():
            exists = User.query.filter(
                (User.username == form.username.data) | (User.email == form.email.data)
            ).first()
            if exists:
                flash("Username or email already registered.", "danger")
                return redirect(url_for("register"))
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("login"))
        if request.method == "POST":
            print("Form data:", request.form)
            print("Form errors:", form.errors)
        return render_template("register.html", form=form)

    @app.route("/auth/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("index"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter(
                or_(User.username == form.username.data, User.email == form.username.data)
            ).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                flash("Logged in successfully.", "success")
                next_page = request.args.get("next") or url_for("index")
                return redirect(next_page)
            flash("Invalid credentials.", "danger")
        return render_template("login.html", form=form)

    @app.route("/auth/logout")
    @login_required
    def logout():
        logout_user()
        flash("You have been logged out.", "info")
        return redirect(url_for("index"))

    return app