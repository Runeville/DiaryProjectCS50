from flask import Flask, redirect, render_template, request, session, flash, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, create_emotions, note_intro, fdatetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc
from database import init_db, db_session
from models import User, Note, Emotion, NoteEmotion


app = Flask(__name__)
app.secret_key = 'key'

app.jinja_env.filters["note_intro"] = note_intro
app.jinja_env.filters["datetime"] = fdatetime


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diary.db"

EMOTIONS = [
    ("Angry", "rgb(240, 91, 97)"), ("Happy", "rgb(255, 202, 5)"), ("Sad", "rgb(41, 131, 197)"), ("Disgusted", "rgb(137, 115, 179)"), ("Feared", "rgb(0, 165, 81)"), ("Annoyed", "rgb(240, 91, 97)"), ("Bored", "rgb(137, 115, 179)")
    ]

init_db()
create_emotions(EMOTIONS, db_session)

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
    emotions = Emotion.query.order_by(Emotion.name).all()
    notes = Note.query.filter(Note.user_id == session["user_id"]).order_by(desc(Note.time_created)).all()
    return render_template("index.html", emotions=emotions, notes=notes)

@app.route("/notes")
@login_required
def notes():
    note_id = request.args.get('id')

    if note_id is not None: # If note is selected
        note = Note.query.filter(Note.user_id == session['user_id']).filter(Note.id == note_id).first()
    else: # Otherwise access last created note
        note = Note.query.filter(Note.user_id == session['user_id']).order_by(desc(Note.time_created)).first()

    # If note not found, flash an error
    if note is None:
        flash("Note not found or access denied")
        return redirect(url_for("index"))
    
    # Find emotions connected to this note
    note_emotions = NoteEmotion.query.filter(NoteEmotion.note_id == note.id).all()
    emotion_ids = [i.emotion_id for i in note_emotions]
    emotions = Emotion.query.filter(Emotion.id.in_(emotion_ids)).order_by(Emotion.name).all()
    
    notes = Note.query.filter(Note.user_id == session["user_id"]).order_by(desc(Note.time_created)).all()
    
    return render_template("notes.html", current_note=note, notes=notes, emotions=emotions)


@app.route("/take-note", methods=["POST"])
def take_note():
    text = request.form.get("note").strip()
    emotions = request.form.getlist("emotion")

    if not text:
        return redirect(url_for("index"))
    
    note = Note(text=text, user_id=session["user_id"])

    try:
        db_session.add(note)
        db_session.commit()
    except:
        flash("Something went wrong")
        return redirect(url_for("index"))
    
    #If okay — add emotions to note
    finally:
        for emotion in emotions:
            emotion = Emotion.query.filter(Emotion.name == emotion).first()
            if emotion is not None:
                db_session.add(NoteEmotion(note_id=note.id, emotion_id=emotion.id))
            
        db_session.commit()

    return redirect(url_for("index"))


@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    
    # If user tries to log in
    username = request.form.get("username").strip()
    password = request.form.get("password").strip()

    if not (username and password):
        flash("All fields must be filled")
        return redirect(url_for("login"))
    
    #If user not found or password doesn't match
    user = User.query.filter(User.username == username).first()
    if user is None or not check_password_hash(user.password, password):
        flash("Invalid username or password")
        return redirect(url_for("login"))
    
    session.clear()
    session["user_id"] = User.query.filter(User.username == username).first().id

    return redirect(url_for("index"))


@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    
    # If user tries to register
    username = request.form.get("username").strip()
    password = request.form.get("password").strip()
    confirm_password = request.form.get("confirm_password").strip()

    # If user didn't input everything
    if not (username and password and confirm_password):
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
    
    session.clear()
    session["user_id"] = User.query.filter(User.username == username).first().id

    return redirect(url_for("index"))
    

@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("index"))
