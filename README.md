# Emotions Diary
## Video Demo:  https://www.youtube.com/watch?v=yGjiNsFg_2c
## Description


### Intro

This is a web-application of **emotions diary** made as a project for CS50 course. People use emotions diary to understand what they feel if they are in need of deeper understanding of their emotions. 

There are several "techniques" of writing this type of diary but I've chosen a really simple one. All the user has to do is to write a **note** on how something went (maybe, they bought a car, or broke up with someone, or talked to a very annoying person), then choose **emotions** that they feel about it from a list and save the note. When time comes and they want to review the note they can find it in notes history.


### Toolkit

- I used python and flask for server side. 
- SQLAlchemy is used to handle database.
- HTML, CSS and JS for styling.


### Files

#### `app.py`
This file contains:
1. All flask and Jinja configurations
2. Logic for all routes and main functions to handle the application
3. EMOTIONS list that contains all emotion names and colors associated with them

Here are additional Jinja filters declared in app.py:
```python
from helpers import note_intro, fdatetime

app.jinja_env.filters["note_intro"] = note_intro
app.jinja_env.filters["datetime"] = fdatetime
```

Functions:
1. `index()` renders `index.html` that gives us a textarea to write notes. It also collects all the notes that are already written by user and puts it into sidebar.
2. `notes()` renders `notes.html`, that is similar to previous html page, but textarea is not editable. This functions puts picked note's text into textarea.
3. `take_note()` has only POST method. It takes note.text and note.emotions as input and INSERTs it into a database. Then redirects to index's url.
4. `login()` in GET method renders `login.html`. Given POST method, logs user in. Sessions are used to keep logged in.
    - `session.clear()` logs user out
    - `session['user_id']` saves user's id on server side to keep them logged.
5. `register()` registers user in and INSERTs values into database.

    If user with same username already exists, I handle it with try block and `IntegrityError` built in `SQLAclhemy.exc`
```python
from sqlalchemy.exc import IntegrityError

try:
        db_session.add(user)
        db_session.commit()
    except IntegrityError:
        flash("This username has already been taken")
        return redirect(url_for("register"))
```

6. `logout()` uses `session.clear()` to clear sessions. Then redirects to index.


#### `helpers.py`
This file contains some secondary functions:
1. `login_required()` restricts user from pages wraped in this functions.
2. `create_emotions()` takes EMOTIONS list as an input. It goes through this list and INPUT every emotion in it if does not exist already.
3. `note_intro()` and `fdatetime()` are filters for Jinja

#### `database.py`
This file contains the declaration of SQLAlchemy engine and Base model

#### `models.py`
This file contains all the models for SQLAlchemy to handle database

#### `static/script.js`
This script makes dynamic coloring of emotions labels. When user clicks on some emotions this script check hidden checkbox and change the label's color. When user click again it removes all the changes described above.

### Database
Database for this project includes several tables, described in `models.py`.

- 'users' contains `id`, `username` and hashed `password`.
- 'notes' contains `id`, `text`, `time_created` (has default value __now()__), `user_id` that is a foreign key to `id` in 'users'.
- 'emotions' contains `id`, `name`, `color` in css format.
- 'notes_emotions' connects tables 'notes' and 'emotions'. It has `id`,  `note_id` that is foreign key to `id` in 'notes', `emotion_id` that is foreign key to `id` in 'emotions'. 


### Installation
To set up and run this project locally, follow these steps:
1. Clone the repository:
```
git clone https://github.com/Runeville/DiaryProjectCS50.git
```
2. Navigate into the project directory:
```
cd DiaryProjectCS50
```
3. Install libraries:
```
pip install -r requirements.txt
```

4. Run flask local server:
```
flask run
```
When done, diary.db should appear in the folder. You can change the name of database in `database.py` and in `app.py`.

If in need to deploy, check flask documentaion on deploying. Also don't forget to set a secret key in `app.py`.
