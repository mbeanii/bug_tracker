from flask import Flask, request, render_template
from database.titanic_db import Database
from paths import DB_PATH
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html", title="Welcome")

@app.route("/open_bugs")
def open_bugs():
    database = Database("bug_tracker", DB_PATH)
    return f"<p>Open Bug Titles: {escape(database.get_open_bugs())}</p>"

@app.route("/bug_details", methods =["GET", "POST"])
def bug_details():
    if request.method == "POST":
        database = Database("bug_tracker", DB_PATH)
        # getting input with name = fname in HTML form
        bug_id = request.form.get("bug_id")
        return "Your bug details " + str(database.get_bug_details_by_id(bug_id))
    return render_template("form.html")
