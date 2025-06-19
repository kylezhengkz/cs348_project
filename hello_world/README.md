# Hello World

[![Static Badge](https://img.shields.io/badge/PostgreSQL-336690?style=for-the-badge)](https://www.postgresql.org/)
[![Static Badge](https://img.shields.io/badge/Python-254F72?style=for-the-badge)](https://www.python.org/downloads/)

<br>

- A simple "hello world" project with PostgreSQL, Flask, and web interface.
- Supports ability to auto-populate table, clear table, and search by user name.
- Uses toy dataset (does not reflect actual project dataset/schema).

### Prerequisites:
- Assumes installation of Python 3.12.10
- Assumes installation of Poetry

<br>

### Run Instructions:
- Create a .env file with database credentials in the project root folder
- Open terminal in project root
```
poetry install
poetry run gunicorn hello_world.app:app
```

<br>
<br>

## How to Create Raw Datasets

Our datasets are synthetically generated.

A dataset is a folder that contains many .csv files. 
For simplicity each .csv file references a particular table in the database.

> [!NOTE]
> The id keys within a dataset are only for convenience for debugging.
> The ids will be regenerated on the dataase side

> [!NOTE]
> Datetimes within the database are assumed to be in UTC timezone.
> Similarly, datetimes within the .csv files are expected to be in UTC timezone.