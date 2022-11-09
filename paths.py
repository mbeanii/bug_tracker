import os

THIS_DIRECTORY = str(os.path.realpath(os.path.dirname(__file__)))
DB_PATH = os.path.join(THIS_DIRECTORY, "database", "bug_tracker.db")
BUGS_CONFIG_PATH = os.path.join(THIS_DIRECTORY, "schema", "bugs", "bugs.json")
BUGS_SCHEMA_PATH = os.path.join(THIS_DIRECTORY, "schema", "bugs", "bugs_schema.json")
USERS_CONFIG_PATH = os.path.join(THIS_DIRECTORY, "schema", "users", "users.json")
USERS_SCHEMA_PATH = os.path.join(THIS_DIRECTORY, "schema", "users", "users_schema.json")
