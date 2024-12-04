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
        #if emotion doesn't exist yet — add new emotion
        if Emotion.query.filter(Emotion.name == emotion[0]).first() is None:
            db_session.add(Emotion(name=emotion[0], color=emotion[1]))

    db_session.commit()
