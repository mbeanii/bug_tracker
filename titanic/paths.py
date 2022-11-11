import os

ROOT_DIRECTORY = str(os.path.realpath(os.path.dirname(__file__)))
DB_PATH = os.path.join(ROOT_DIRECTORY, "database", "bug_tracker.db")
BUGS_CONFIG_PATH = os.path.join(ROOT_DIRECTORY, "schema", "bugs", "bugs.json")
BUGS_SCHEMA_PATH = os.path.join(ROOT_DIRECTORY, "schema", "bugs", "bugs_schema.json")
USERS_CONFIG_PATH = os.path.join(ROOT_DIRECTORY, "schema", "users", "users.json")
USERS_SCHEMA_PATH = os.path.join(ROOT_DIRECTORY, "schema", "users", "users_schema.json")
IMAGES_DIRECTORY = os.path.join(ROOT_DIRECTORY, "wsgi", "static")
PHOTO_PATH = os.path.join(IMAGES_DIRECTORY, "titanic.jpg")