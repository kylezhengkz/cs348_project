# Room Booking App Backend Server

[![Static Badge](https://img.shields.io/badge/PostgreSQL-336690?style=for-the-badge)](https://www.postgresql.org/)
[![Static Badge](https://img.shields.io/badge/Python-254F72?style=for-the-badge)](https://www.python.org/downloads/)

The backend API for the room booking app.

<br>

## How to Run

### Step 1:
Run the following command and replace `[env]` with either `prod`, `dev` or `toy`, depending on the environment
you are running.

```
Poetry run python main.py -e [env]
```

<br>

### Step 2:
Now the backend API is running in the following URLs for the given environment:

| Environment | Port |
| ----------- | ---- |
| Production | http://localhost:9012 |
| Development | http://localhost:9011 |
| Toy | http://localhost:9013 |

<br>

## Command Options

Below are the command options available for running the backend:

```
-h, --help         show this help message and exit
-e str, --env str  What environment mode we want to run the backend. 
                   Available modes are: 'prod', 'dev' and 'toy'

                   By default, 'toy' is selected
-d, --debug        Whether to turn on debugging mode. By default, this debug mode is turned off.
```
