from uuid import uuid4
import pendulum
from database.titanic_db import Titanic
from flask import Flask, render_template, request, jsonify
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template("welcome.html", title="Welcome")

@app.route("/open_bugs")
def open_bugs():
    """ Requirement 1 """
    database = Titanic()
    return render_template("open_bugs.html", result=database.get_open_bugs())

@app.route("/bug_details", methods =["GET", "POST"])
def bug_details():
    """ Requirement 2 """
    database = Titanic()
    if request.method == "POST":
        bug_id = request.form.get("bug_id").strip()

        # Validate input
        if bug_id not in database.get_all_bugs().keys():
            return render_template("invalid_entry.html")
        
        return render_template("bug_details.html", result=database.get_bug_details_by_id(bug_id))
    return render_template("bug_details_form.html", result=database.get_all_bugs())

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
        # TODO: Validate inputs against schema (see /design#Further Improvements)
        
        # Validate inputs
        if not details["title"]:
            return render_template("invalid_entry.html")
        
        database.add_table_entry("bugs", details)
        return "Your bug id " + escape(details["id"])
    return render_template("create_bug_form.html")

@app.route("/close_bug", methods =["GET", "POST"])
def close_bug():
    """ Requirement 4 """
    database = Titanic()
    if request.method == "POST":
        mods = {
            "status": "closed",
        }
        bug_id = request.form.get("bug_id").strip()

        # Validate input
        if bug_id not in database.get_all_bugs().keys():
            return render_template("invalid_entry.html")
        
        response = database.modify_bug_by_id(bug_id, mods)
        if response:
            return "Bug id " + escape(bug_id) + " successfully modified."
        else:
            return "Something went wrong while attempting to modify bug id " + escape(bug_id)
    return render_template("close_bug_form.html", result=database.get_open_bugs())

@app.route("/assign_bug", methods =["GET", "POST"])
def assign_bug():
    """ Requirement 5 """
    database = Titanic()
    user_list = database.get_all_users()
    if request.method == "POST":
        bug_id = request.form.get("bug_id").strip()
        owner_id = request.form.get("owner_id").strip()

        # Validate inputs
        if  bug_id not in database.get_all_bugs().keys()\
            or owner_id not in user_list.keys():
            return render_template("invalid_entry.html")
        
        mods = {
            "owner_id": owner_id,
        }
        # TODO: Validate inputs against schema (see /design#Further Improvements)

        response = database.modify_bug_by_id(bug_id, mods)
        if response:
            return "Bug id " + escape(bug_id) + " successfully assigned to " + escape(owner_id) + "."
        else:
            return "Something went wrong."
    return render_template("assign_bug_form.html", bugs=database.get_open_bug_owners(), users=user_list)

@app.route("/add_user", methods =["GET", "POST"])
def add_user():
    """ Requirement 6 """
    database = Titanic()
    all_users = database.get_all_users()
    if request.method == "POST":
        owner_name = request.form.get("owner_name").strip()

        # Validate input
        if  owner_name in all_users.keys()\
            or not owner_name:
            return render_template("invalid_entry.html")
        
        details = {
            "id": str(uuid4()),
            "name": owner_name
        }
        database.add_table_entry("users", details)
        return f"User {escape(owner_name)} Added with user id {escape(details['id'])}"
    return render_template("add_user_form.html", result=all_users)

@app.route("/change_username", methods =["GET", "POST"])
def change_username():
    """ Requirement 7 """
    database = Titanic()
    all_users = database.get_all_users()
    # See todo on add_user above
    if request.method == "POST":
        owner_id = request.form.get("owner_id").strip()
        new_name = request.form.get("new_name").strip()

        # Validate inputs
        if  owner_id not in all_users.keys()\
            or not new_name\
            or new_name in all_users.values():
            return render_template("invalid_entry.html")

        details = {
            "name": new_name
        }
        database.update_table_row("users", details, "id", owner_id)
        return f"User {escape(owner_id)} name changed to {escape(new_name)}"
    return render_template("change_username_form.html", result=all_users)

@app.route("/beauty")
def beauty():
    """ Requirement 8 """
    return render_template("beauty.html")

@app.route("/api/open_bugs")
def api_open_bugs():
    """ Requirement 9 """
    database = Titanic()
    return jsonify(database.get_open_bugs())

@app.route("/design")
def design():
    """ Requirement 10 """
    return render_template("design.html")