from database.titanic_db import Titanic

if __name__ == '__main__':
    db = Titanic()
    c = db.conn.cursor()

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
    print(db.get_open_bugs())

    print("Get bug details by id (d08e099e-6686-4a5a-ab43-0338b9adaf4b): ")
    print(db.get_bug_details_by_id("d08e099e-6686-4a5a-ab43-0338b9adaf4b"))


    mods = {
        "status": "closed",
    }
    bug_id = "d08e099e-6686-4a5a-ab43-0338b9adaf4b"
    response = db.modify_bug_by_id(bug_id, mods)
    if response:
        print("Bug " + bug_id + " successfully closed.")
    else:
        print("Something went wrong while attempting to modify bug " + bug_id)