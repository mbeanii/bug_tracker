import sqlite3
import json
from jsonschema import validate
from paths import BUGS_JSON_SCHEMA_PATH, USERS_JSON_SCHEMA_PATH

def push_bug(conn: sqlite3.Connection, bug: dict) -> None:
    """ Adds a bug to the bugs table
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object
        bug  (dict)               : A dict following the bugs_schema

    Returns:
        Nothing
    
    Raises:
        jsonschema.exceptions.ValidationError if bug does not follow bugs_schema
    """
    bugs_schema = None
    with open(BUGS_JSON_SCHEMA_PATH) as f:
        bugs_schema = json.loads(f.read())
    validate(schema=bugs_schema, instance=[bug])

    c = conn.cursor()
    query = f'''
            INSERT INTO bugs ({str(list(bug.keys()))[1:-1]})

                    VALUES
                    ({str(list(bug.values()))[1:-1]})
            '''
    c.execute(query)


def push_user(conn: sqlite3.Connection, user: dict) -> None:
    """ Adds a user to the users table
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object
        user  (dict)               : A user following the users_schema

    Returns:
        Nothing
    
    Raises:
        jsonschema.exceptions.ValidationError if user does not follow users_schema
    """
    users_schema = None
    with open(USERS_JSON_SCHEMA_PATH) as f:
        users_schema = json.loads(f.read())
    validate(schema=users_schema, instance=[user])

    c = conn.cursor()
    query = f'''
            INSERT INTO users ({str(list(user.keys()))[1:-1]})

                    VALUES
                    ({str(list(user.values()))[1:-1]})
            '''
    c.execute(query)


def get_open_bugs(conn: sqlite3.Connection) -> list:
    """ Fetches a list of open bug titles, per req #1
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object

    Returns:
        A list of string values - titles of open bugs
    
    Raises:
        Nothing
    """
    c = conn.cursor()
    res = c.execute("SELECT title FROM bugs WHERE status='open'")
    return res.fetchall()


def get_bug_details_by_id(conn: sqlite3.Connection, id_: str) -> dict:
    """ Fetches bug details for an individual bug, per req #2
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object
        id_ (str)                 : A UUID

    Returns:
        A dictionary containing the following keys:
            {
                "title": "X",
                "description": "Y",
                "opened_on": "1970-01-01T00:00:00+00:00"
            }
    
    Raises:
        Nothing
    """
    c = conn.cursor()
    res = c.execute(f"SELECT title, description, opened_on FROM bugs WHERE id='{id_}'")
    results = res.fetchall()[0]
    return {
        "title": results[0],
        "description": results[1],
        "opened_on": results[2]
    }
