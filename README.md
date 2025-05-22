# CS 348 Project

[![Static Badge](https://img.shields.io/badge/PostgreSQL-336690?style=for-the-badge)](https://www.postgresql.org/)
[![Static Badge](https://img.shields.io/badge/Python-254F72?style=for-the-badge)](https://www.python.org/downloads/)

<br>

## Members
|     |     |
| --- | --- |
| **Alex Au** | https://github.com/Alex-Au1 |
| **Anika Awasthi** | https://github.com/anikawas |
| **Ananya Ohrie** | https://github.com/ananyao3 |
| **Anthony Tieu** | https://github.com/Akali404 |
| **Kyle Zheng** | https://github.com/kylezhengkz |

<br>

## Hello World
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


### Step 1.
Create a new folder for the dataset at [Tools/DataImporter/data](Tools/DataImporter/data)

<br>

### Step 2.
Create the corresponding .csv files based on the tables within the databases

<br>
<br>

## How to Load Datasets to the Database

Follow the instructions at [Tools/DataImporter](Tools/DataImporter/README.md)
