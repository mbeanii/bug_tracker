import json
from jsonschema import validate
import sqlite3
from paths import DB_PATH, BUGS_CONFIG_PATH, BUGS_SCHEMA_PATH, USERS_CONFIG_PATH, USERS_SCHEMA_PATH
from os.path import exists

class Table():
    """ Class for managing table initialization values."""
    def __init__(self, name: str, config_path, schema_path):
        """Retrieves a config and schema and performs validation. """
        self.name = name
        self.config_path = config_path
        self.schema_path = schema_path
        with open(config_path) as f:
            self.config = json.loads(f.read())
        with open(schema_path) as f:
            self.schema = json.loads(f.read())
        validate(instance=self.config, schema=self.schema)


class Database():
    """ Database management class """
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.conn = sqlite3.connect(path)
        self.table_titles = self.get_table_titles()
    
    def __del__(self):
        self.conn.close()

    def add_table(self, name: str, config_path, schema_path):
        if name not in self.table_titles:
            self.table_titles.append(name)
            table = Table(name, config_path, schema_path)
            self.instantiate_table(table.schema, table.name)
            for row in table.config:
                self.add_table_entry(table.name, row)

    def instantiate_table(self, schema: dict, table_name: str) -> None:
        """ Instantiates a db table
        
        Inputs:
            schema     (dict)         : A json schema dict
            table_name (str)          : The desired table name

        Returns:
            Nothing
        
        Raises:
            Nothing
        """
        c = self.conn.cursor()

        # Fetch properties from schema
        keys = [[key] for key in schema["items"][0]["properties"].keys()]

        # Format as columns for query
        keys_str = str(keys)[1:-1].replace("'","")
        
        c.execute(f'''
                CREATE TABLE IF NOT EXISTS {table_name}
                ({keys_str})
                ''')
        self.conn.commit()    

    def add_table_entry(self, table_name: str, entry: dict) -> None:
        """ Adds a db table entry (may be used to satisfy req #3/6)
        
        Inputs:
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

        c = self.conn.cursor()
        query = f'''
                INSERT INTO {table_name} ({entry_keys_str})

                        VALUES
                        ({entry_values_str})
                '''
        c.execute(query)
        self.conn.commit()
        return

    def get_table_titles(self) -> list:
        """ Fetches a list of table titles
        
        Inputs:
            None

        Returns:
            A list of string values - titles of db tables
        
        Raises:
            Nothing
        """
        c = self.conn.cursor()
        res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tuple_list = res.fetchall()
        return [tuple[0] for tuple in tuple_list]


    def get_open_bugs(self) -> list:
        """ Fetches a list of open bug titles, per req #1
        
        Inputs:
            None

        Returns:
            A list of string values - titles of open bugs
        
        Raises:
            Nothing
        """
        c = self.conn.cursor()
        res = c.execute("SELECT title FROM bugs WHERE status='open'")
        tuple_list = res.fetchall()
        return [tuple[0] for tuple in tuple_list]


    def get_bug_details_by_id(self, id_: str) -> dict:
        """ Fetches bug details for an individual bug, per req #2
        
        Inputs:
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
        c = self.conn.cursor()
        res = c.execute(f"SELECT title, description, opened_on FROM bugs WHERE id='{id_}'")
        results = res.fetchall()[0]
        return {
            "title": results[0],
            "description": results[1],
            "opened_on": results[2]
        }

    def modify_bug_by_id(self, id_: str) -> dict:
        """ Changes one or more attributes for an individual bug, per req #4/5
        
        Inputs:
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
        c = self.conn.cursor()
        res = c.execute(f"SELECT title, description, opened_on FROM bugs WHERE id='{id_}'")
        results = res.fetchall()[0]
        return {
            "title": results[0],
            "description": results[1],
            "opened_on": results[2]
        }

if __name__ == '__main__':
    database = Database("bug_tracker", DB_PATH)
    if not exists(DB_PATH):
        database.add_table("bugs", BUGS_CONFIG_PATH, BUGS_SCHEMA_PATH)
        database.add_table("users", USERS_CONFIG_PATH, USERS_SCHEMA_PATH)
