import os

THIS_DIRECTORY = str(os.path.realpath(os.path.dirname(__file__)))
DB_PATH = os.path.join(THIS_DIRECTORY, "bug_tracker.db")
BUGS_JSON_PATH = os.path.join(THIS_DIRECTORY, "..", "schema", "bugs", "bugs.json")
BUGS_JSON_SCHEMA_PATH = os.path.join(THIS_DIRECTORY, "..", "schema", "bugs", "bugs_schema.json")
USERS_JSON_PATH = os.path.join(THIS_DIRECTORY, "..", "schema", "users", "users.json")
USERS_JSON_SCHEMA_PATH = os.path.join(THIS_DIRECTORY, "..", "schema", "users", "users_schema.json")
