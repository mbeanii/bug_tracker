from uuid import uuid4
import pendulum
from database.titanic_db import Titanic
from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from paths import PHOTO_PATH

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html", title="Welcome")

@app.route("/open_bugs")
def open_bugs():
    """ Requirement 1 """
    database = Titanic()
    return f"<p>Open Bug Titles: {escape(database.get_open_bugs())}</p>"

@app.route("/bug_details", methods =["GET", "POST"])
def bug_details():
    """ Requirement 2 """
    if request.method == "POST":
        database = Titanic()
        bug_id = request.form.get("bug_id")
        return "Your bug details " + str(database.get_bug_details_by_id(bug_id))
    return render_template("bug_details_form.html")

@app.route("/create_bug", methods =["GET", "POST"])
def create_bug():
    """ Requirement 3 """
    if request.method == "POST":
        database = Titanic()
        details = {
            "id": str(uuid4()),
            "opened_on": pendulum.now().to_iso8601_string(),
            "title": request.form.get("title"),
            "description": request.form.get("description"),
            "status": "open",
            "owner_id": ""
        }
        database.add_table_entry("bugs", details)
        return "Your bug id " + escape(details["id"])
    return render_template("create_bug_form.html")

@app.route("/close_bug", methods =["GET", "POST"])
def close_bug():
    """ Requirement 4 """
    if request.method == "POST":
        database = Titanic()
        mods = {
            "status": "closed",
        }
        bug_id = request.form.get("bug_id")
        response = database.modify_bug_by_id(bug_id, mods)
        if response:
            return "Bug id " + escape(bug_id) + " successfully modified."
        else:
            return "Something went wrong while attempting to modify bug id " + escape(bug_id)
    return render_template("close_bug_form.html")

@app.route("/assign_bug", methods =["GET", "POST"])
def assign_bug():
    """ Requirement 5 """
    if request.method == "POST":
        database = Titanic()
        bug_id = request.form.get("bug_id")
        owner_id = request.form.get("owner_id")
        # TODO: Verify exists in the db 
        mods = {
            "owner_id": owner_id,
        }
        response = database.modify_bug_by_id(bug_id, mods)
        if response:
            return "Bug id " + escape(bug_id) + " successfully assigned to " + escape(owner_id) + "."
        else:
            return "Something went wrong."
    return render_template("assign_bug_form.html")

@app.route("/add_user", methods =["GET", "POST"])
def add_user():
    """ Requirement 6 """
    # TODO: There's currently no front-end accessible way to verify the change
    # (database/tests.py prints users from the db)
    if request.method == "POST":
        database = Titanic()
        owner_name = request.form.get("owner_name")
        details = {
            "id": str(uuid4()),
            "name": owner_name
        }
        database.add_table_entry("users", details)
        return f"User {escape(owner_name)} Added with user id {escape(details['id'])}"
    return render_template("add_user_form.html")

@app.route("/change_username", methods =["GET", "POST"])
def change_username():
    """ Requirement 7 """
    # See todo on add_user above
    if request.method == "POST":
        database = Titanic()
        owner_id = request.form.get("owner_id")
        new_name = request.form.get("new_name")
        details = {
            "name": new_name
        }
        database.update_table_row("users", details, "id", owner_id)
        return f"User {escape(owner_id)} name changed to {escape(new_name)}"
    return render_template("change_username_form.html")

@app.route("/beauty")
def beauty():
    """ Requirement 8 """
    return render_template("beauty.html")

@app.route("/api/open_bugs")
def api_open_bugs():
    """ Requirement 9 """
    database = Titanic()
    return jsonify(database.get_open_bugs())

@app.route("/database")
def database():
    """ Requirement 10 """
    return render_template("database.html")