# CS 348 Project

[![Static Badge](https://img.shields.io/badge/React-09d9fe?style=for-the-badge)](https://react.dev/)
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

### Prerequisites:
- Python 3.12.10
- Poetry
- Node.js 16+

Install all the Python dependencies for the project by running the command:
```
Poetry install
```

<br>

## Room Booking App
The app has the 3 types of environment modes:

<br>

| Environment Name | Description |
| ---------------- | ----------- |
| Production | Contains the production dataset |
| Development | Contains the sample dataset |
| Toy | Contains the toy dataset |

<br>

Also, the app is split into a frontend and a backend to follow a client-server architecture. 
See the links below on instructions for how to run each part:

- [Client Frontend](frontend/README.md)
- [Backend Server](backend/README.md)

<br>

## Hello World App
A very basic app to test connection to the database.
For more info, you can visit [hello_world](hello_world/README.md)

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

<br>

### Step 1.
Create a new folder for the dataset at [Tools/DataImporter/data](Tools/DataImporter/data)

<br>

### Step 2.
Create the corresponding .csv files based on the tables within the databases

<br>
<br>

## How to Load Datasets to the Database

Follow the instructions at [Tools/DataImporter](Tools/DataImporter/README.md)
