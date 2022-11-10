""" Initializes titanic.db """

import json
from jsonschema import validate

import sqlite3
from database.db_queries import instantiate_table, get_table_titles, add_table_entry
from paths import DB_PATH, BUGS_CONFIG_PATH, BUGS_SCHEMA_PATH, USERS_CONFIG_PATH, USERS_SCHEMA_PATH

class Table():
    def __init__(self, name: str, config_path, schema_path):
        self.name = name
        self.config_path = config_path
        self.schema_path = schema_path
        with open(config_path) as f:
            self.config = json.loads(f.read())
        with open(schema_path) as f:
            self.schema = json.loads(f.read())
        validate(instance=self.config, schema=self.schema)


class Database():
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.conn = sqlite3.connect(path)
        self.table_titles = get_table_titles(self.conn)
    
    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def add_table(self, name: str, config_path, schema_path):
        if name not in self.table_titles:
            self.table_titles.append(name)
            table = Table(name, config_path, schema_path)
            instantiate_table(self.conn, table.schema, table.name)
            for row in table.config:
                add_table_entry(self.conn, table.name, row)


if __name__ == '__main__':
    database = Database("bug_tracker", DB_PATH)
    database.add_table("bugs", BUGS_CONFIG_PATH, BUGS_SCHEMA_PATH)
    database.add_table("users", USERS_CONFIG_PATH, USERS_SCHEMA_PATH)
