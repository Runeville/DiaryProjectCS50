from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username!r}>'
    

class Note(Base):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))

    def __init__(self, text=None, user_id=None):
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f'<Note at {self.time_created!r}: "{self.text!r}">'


class Emotion(Base):
    __tablename__ = 'emotions'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), unique=True, nullable=False)
    color = Column(String(15), nullabe=False)

    def __init__(self, name=None, color=None):
        self.name = name
        self.color = color

    def __repr__(self):
        return f'<Emotion {self.name!r}>'


class NoteEmotion(Base):
    __tablename__ = 'notes_emotions'

    id = Column(Integer, primary_key=True)
    note_id = Column(Integer, ForeignKey(Note.id))
    emotion_id = Column(Integer, ForeignKey(Emotion.id))

    def __init__(self, note_id=None, emotion_id=None):
        self.note_id = note_id
        self.emotion_id = emotion_id

    def __repr__(self):
        return f'<Emotion {self.emotion_id!r} to note {self.note_id!r}>'
