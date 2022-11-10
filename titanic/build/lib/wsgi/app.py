from flask import Flask
from database.titanic_db import Database
from paths import DB_PATH
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def welcome():
    return f"<p>Welcome to the Titanic bug tracker</p>"

@app.route("/table_titles")
def table_titles():
    database = Database("bug_tracker", DB_PATH)
    return f"<p>Table Titles: {escape(database.get_table_titles())}!</p>"

@app.route("/open_bugs")
def open_bugs():
    database = Database("bug_tracker", DB_PATH)
    return f"<p>Table Titles: {escape(database.get_open_bugs())}!</p>"
