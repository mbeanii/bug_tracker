import sqlite3

def instantiate_table(conn: sqlite3.Connection, schema: dict, table_name: str) -> None:
    """ Instantiates a db table
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object
        schema     (dict)         : A json schema dict
        table_name (str)          : The desired table name

    Returns:
        Nothing
    
    Raises:
        Nothing
    """
    c = conn.cursor()

    # Fetch properties from schema
    keys = [[key] for key in schema["items"][0]["properties"].keys()]

    # Format as columns for query
    keys_str = str(keys)[1:-1].replace("'","")
    
    c.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name}
            ({keys_str})
            ''')
    conn.commit()    

def add_table_entry(conn: sqlite3.Connection, table_name: str, entry: dict) -> None:
    """ Adds a db table entry (may be used to satisfy req #3/6)
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object
        table_name  (str)         : The nambe of a db table
        entry  (dict)             : A single dict to be added

    Returns:
        Nothing
    
    Raises:
        Nothing
    """

    entry_keys = list(entry.keys())
    # Remove [] from list to format query
    entry_keys_str = str(entry_keys)[1:-1]

    entry_values = list(entry.values())
    # Remove [] from list to format query
    entry_values_str = str(entry_values)[1:-1]

    c = conn.cursor()
    query = f'''
            INSERT INTO {table_name} ({entry_keys_str})

                    VALUES
                    ({entry_values_str})
            '''
    c.execute(query)
    return

def get_table_titles(conn: sqlite3.Connection) -> list:
    """ Fetches a list of table titles
    
    Inputs:
        conn (sqlite3.Connection) : A sqlite3 connection object

    Returns:
        A list of string values - titles of db tables
    
    Raises:
        Nothing
    """
    c = conn.cursor()
    res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tuple_list = res.fetchall()
    return [tuple[0] for tuple in tuple_list]


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
    tuple_list = res.fetchall()
    return [tuple[0] for tuple in tuple_list]


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

def modify_bug_by_id(conn: sqlite3.Connection, id_: str) -> dict:
    """ Changes one or more attributes for an individual bug, per req #4/5
    
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