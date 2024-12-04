from functools import wraps
from flask import render_template, redirect, session

from models import Emotion


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def create_emotions(emotions:list, db_session):
    for emotion in emotions:
        Emotion.query.filter(Emotion.name == emotion).first()
        if Emotion.query.filter(Emotion.name == emotion).first() is None:
            db_session.add(Emotion(name=emotion))

    db_session.commit()


    #TODO: if already exists
