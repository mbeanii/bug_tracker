""" Initializes titanic.db """

import sqlite3
import json
from db_queries import push_bug, push_user
from paths import DB_PATH, BUGS_JSON_PATH, BUGS_JSON_SCHEMA_PATH, USERS_JSON_PATH, USERS_JSON_SCHEMA_PATH

def instantiate_tables(conn: sqlite3.Connection) -> None:
    """ Instantiates db tables
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object

    Returns:
        Nothing
    
    Raises:
        Nothing
    """
    c = conn.cursor()

    # Dynamically fetch bugs columns
    with open(BUGS_JSON_SCHEMA_PATH) as f:
        bugs_schema = json.loads(f.read())
    bug_keys = str( [[key] for key in bugs_schema["items"][0]["properties"].keys()] )[1:-1].replace("'","")
    
    c.execute(f'''
            CREATE TABLE IF NOT EXISTS bugs
            ({bug_keys})
            ''')
    conn.commit()

    # Dynamically fetch users columns
    with open(USERS_JSON_SCHEMA_PATH) as f:
        users_schema = json.loads(f.read())
    user_keys = str( [[key] for key in users_schema["items"][0]["properties"].keys()] )[1:-1].replace("'","")
    
    c.execute(f'''
            CREATE TABLE IF NOT EXISTS users
            ({user_keys})
            ''')
    conn.commit()
    

if __name__ == '__main__':
    with sqlite3.connect(DB_PATH) as connection:
        
        instantiate_tables(connection)
        
        with open(BUGS_JSON_PATH) as f:
            bugs = json.loads(f.read())
            for bug in bugs:
                push_bug(connection, bug)
        
        with open(USERS_JSON_PATH) as f:
            users = json.loads(f.read())
            for user in users:
                push_user(connection, user)
