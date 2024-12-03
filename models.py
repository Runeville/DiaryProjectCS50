from sqlalchemy import Column, Integer, String, Text
from database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(15), unique=True)
    password = Column(Text())

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User {self.username!r}>'
    
