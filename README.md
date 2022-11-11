# bug_tracker
Welcome to the Titanic bug tracker.

To run:
1) cd into the wsgi directory
2) Run "python -m flask run"
3) Navigate to http://127.0.0.1:5000/

Local import errors may be resolved by building the package.
To build the package:
1) (recommended) Activate virtual environment "venv"
2) cd into the titanic directory
3) Run pip install -e .

To reinitialize the database:
1) Delete database/bug_tracker.db
2) Navigate to http://127.0.0.1:5000/open_bugs (or any other page that accesses the db)