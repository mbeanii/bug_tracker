import json
from jsonschema import validate
import sqlite3
from paths import DB_PATH, BUGS_CONFIG_PATH, BUGS_SCHEMA_PATH, USERS_CONFIG_PATH, USERS_SCHEMA_PATH
from os.path import exists

class Table():
    """ Class for managing table initialization values. """
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

    def populate_table(self, name: str, config_path: str, schema_path: str):
        """ Adds local config data to a db table
        
        Inputs:
            name        (str) : The table name
            config_path (str) : The file path to a .json config
            schema_path (str) : The file path to a .json schema 

        Returns:
            Nothing
        
        Raises:
            Nothing
        """
        if name not in self.table_titles:
            self.table_titles.append(name)
            table = Table(name, config_path, schema_path)
            self.instantiate_table(table.schema, table.name)
            for row in table.config:
                self.add_table_entry(table.name, row)

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

    def update_table_row(self, table_name: str, modifications: dict, condition_field: str, condition_value: str) -> None:
        """ Updates existing table row(s)
        
        Inputs:
            table_name (str): The name of the table containing the row(s) to be updated
            modifications (dict): A dict of keys/values to be modified
            condition_field (str): The name of the db column
            condition_value (str): If condition_field is set to this value, modify the row

        Returns:
            Nothing
        
        Raises:
            Nothing
        """
        c = self.conn.cursor()
        query = f"UPDATE {table_name}\n"
        add_comma = False
        for key, value in modifications.items():
            if add_comma:
                query += ", "
            query += f"SET {key}='{value}'"
            add_comma = True
        query += f"\nWHERE {condition_field}='{condition_value}';"
        c.execute(query)
        self.conn.commit()
        return


class Titanic(Database):
    """ A top-level class for the Titanic Database """
    def __init__(self):

        init_tables = False
        if not exists(DB_PATH):
            init_tables = True

        super(). __init__("titanic", DB_PATH)

        if init_tables:
            self.populate_table("bugs", BUGS_CONFIG_PATH, BUGS_SCHEMA_PATH)
            self.populate_table("users", USERS_CONFIG_PATH, USERS_SCHEMA_PATH)

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
        res = c.execute("SELECT title FROM bugs WHERE status='open';")
        tuple_list = res.fetchall()
        return [tuple[0] for tuple in tuple_list]


    def get_bug_details_by_id(self, id_: str) -> dict:
        """ Fetches bug details for an individual bug, per req #2
        
        Inputs:
            id_ (str)                 : A UUID

        Returns:
            A dictionary containing the following keys:
                {
                    "opened_on": "1912-01-12T00:00:00+00:00",
                    "title": "Message of initial advertising campaign 'very unlikely to sink' not strong enough.",
                    "description": "Fate unlikely to be tempted. Update: Now resolved.",
                    "status": "closed",
                    "owner_id": "7e1a03e4-569a-4b62-b3ce-2391edd83eb3"
                }
        
        Raises:
            Nothing
        """
        c = self.conn.cursor()
        res = c.execute(f"SELECT opened_on, title, description, status, owner_id FROM bugs WHERE id='{id_}';")
        results = res.fetchall()[0]
        return {
            "opened_on": results[0],
            "title": results[1],
            "description": results[2],
            "status" : results[3],
            "owner_id": results[4]
        }

    def modify_bug_by_id(self, id_: str, modifications: dict) -> None:
        """ Changes one or more attributes for an individual bug, per req #4/5
        
        Inputs:
            id_ (str)                 : A UUID
            modifications (dict)      : A dict of keys/values to be modified.
                May include any of the following:
                {
                    "title": "X",
                    "description": "Y",
                    "status": "open"
                    "owner_id": "96997019-e16e-499f-9053-33ab6e32ec34"
                }

        Returns:
            False if inputs were invalid
            Otherwise True
        
        Raises:
            Nothing
        """
        for key in modifications:
            if  key not in ["title", "description", "status", "owner_id"]:
                return False
        self.update_table_row("bugs", modifications, "id", id_)
        return True

if __name__ == '__main__':
    Titanic()
