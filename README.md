# CS 348 Project

[![Static Badge](https://img.shields.io/badge/React-09d9fe?style=for-the-badge)](https://react.dev/)
[![Static Badge](https://img.shields.io/badge/PostgreSQL-336690?style=for-the-badge)](https://www.postgresql.org/)
[![Static Badge](https://img.shields.io/badge/Python-254F72?style=for-the-badge)](https://www.python.org/downloads/)
[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/Alex-Au1/CampusBookingWebApp/unit-tests.yml?style=for-the-badge&label=Unit%20Tests)](https://github.com/Alex-Au1/CampusBookingWebApp/actions/workflows/unit-tests.yml)

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
<br>

## Prerequisites:
- Python 3.12.10
- Poetry
- Node.js 16+

<br>
<br>

## Setting Up Dependencies:
1. From the project root folder run the commands:
    ```
    poetry lock
    poetry install
    poetry run playwright install
    ```
2. From `frontend/`, run the command:
    ```
    npm install
    ```
3. Create a new file called `.env` in the folder where this README.MD is created. For what parameters to put in this new `.env` file, follow the format specified at [template.env](template.env)

<br>

> [!NOTE]
> For the values of the paramters (eg. database credentials), checkout the credentials mentioned in the report for Milestone 1

<br>
<br>

## Overview
As we transition into Milestone 1, new tools have been developed and old tools have been depreciated.

The following is a list of current apps/tools:
- Room booking app (frontend + backend).
- hello_world: A now depreciated app, previously used for Milestone 0.
- DataImporter: A powerful tool for database setup and administration (i.e., table creation, data importation, etc.).
- DataPopulator: A tool for generating datasets, either artificially or by scraping real-world data. 

<br>
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

Currently supported features include:

- The ability to filter available rooms based on room name, min. and max. capacity, and time-slot.
- The ability to book a room.
- The ability to cancel an existing booking.
- The ability to view future bookings (excluding cancellations). (new in Milestone2)
- The ability to view past bookings (including cancellations). (new in Milestone2)
- The ability to signup/login which is needed to view/book/cancel any booking or room (new in Milestone2).

<br>
<br>

## Hello World App
A very basic app to test connection to the database.
For more info, you can visit [hello_world](hello_world/README.md)

<br>
<br>

## DataImporter: How to Create Raw Datasets

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

## DataImporter: How to Load Datasets to the Database

Follow the instructions at [Tools/DataImporter](Tools/DataImporter/README.md)

<br>
<br>

## DataPopulator: How to Load Production Datasets

To populate the `production` database with data. Run the command:
```
poetry run db_pop -e prod -o -g -p
```
Documentation on all available flags and command line arguments (including those not shown above) are available via:
```
poetry run db_pop -h
```
<br>
<br>

## Quick Start Guide

1. Run `DataImporter` to create tables and constraints.
2. Run `DataPopulator` to add sample data.
3. Run the contents of `backend/`.
4. Run the contents of `frontend/`.
