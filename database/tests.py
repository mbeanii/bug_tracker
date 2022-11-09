import sqlite3
from db_queries import get_open_bugs, get_bug_details_by_id
from sys import path
path.append('../BUG_TRACKER')
from paths import DB_PATH

if __name__ == '__main__':
    with sqlite3.connect(DB_PATH) as connection:
        
        c = connection.cursor()

        res = c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print("Table titles: ")
        print([tuple_[0] for tuple_ in res.fetchall()])

        res = c.execute("SELECT title FROM bugs")
        print("Bug titles: ")
        print(res.fetchall())

        res = c.execute("SELECT name FROM users")
        print("User names: ")
        print(res.fetchall())

        print("Open bugs: ")
        print(get_open_bugs(connection))

        print("Get bug details by id (d08e099e-6686-4a5a-ab43-0338b9adaf4b): ")
        print(get_bug_details_by_id(connection, "d08e099e-6686-4a5a-ab43-0338b9adaf4b"))
