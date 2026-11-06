# AGAProject

A small Flask app for keeping gym client records: name, contact details, membership dates and type, goals, and assigned trainer. Clients can be added through a form and searched by name.

## Stack

- Python, Flask
- Flask-SQLAlchemy with a local SQLite database

## Run it

```bash
pip install flask flask-sqlalchemy
python backend.py
```

The database (`clients.db`) is created locally on first run. It holds personal data, so it is git-ignored and never committed.
