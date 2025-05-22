# cs348_project
Description:
- A simple "hello world" project with PostgreSQL, Flask, and web interface.
- Supports ability to auto-populate table, clear table, and search by user name.
- Uses toy dataset (does not reflect actual project dataset/schema).

Prerequisites:
- Assumes installation of Python 3.12.10
- Assumes installation of Poetry

Run Instructions:
- Create a .env file with database credentials in the project root folder
- Open terminal in project root
- poetry install
- poetry run gunicorn hello_world.app:app
- Open http://127.0.0.1:8000