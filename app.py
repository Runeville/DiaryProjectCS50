import os

from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

from sqlalchemy.exc import IntegrityError
from database import init_db, db_session
from models import User


app = Flask(__name__)
app.secret_key = 'key'


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diary.db"

init_db()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


Session(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    
    # If user tries to register
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    # If user didn't input everything
    if not (username and password and password and confirm_password):
        flash("All fields must be filled")
        return redirect(url_for("register"))
    
    # If passwords don't match redirect to register
    if password != confirm_password:
        flash("Passwords don't match")
        return redirect(url_for("register"))
    
    user = User(username=username, password=generate_password_hash(password))

    # Handling same usernames problem
    try:
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        flash("This username has already been taken")
        return redirect(url_for("register"))

    session["user_id"] = User.query.filter(User.username == username).first().id

    return redirect(url_for("index"))
    


@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("index"))
