import os
import psycopg2
import sys
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DB = os.getenv("DB")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

db_connection = None

def db_open_connection():
    global db_connection
    print(f"{DB} AND {DB_USERNAME} AND{DB_PASSWORD} AND {DB_HOST} AND {DB_PORT}")

    try:
        db_connection = psycopg2.connect(database = DB, user = DB_USERNAME, password = DB_PASSWORD, host = DB_HOST, port = DB_PORT)
        print("[\033[92mOK\033[0m] Open DB Connection")
    except Exception as e:
        db_connection = None
        print(f"HELLO")
        print("[\033[91mFAIL\033[0m] Open DB Connection")
        raise e

def db_close_connection():
    global db_connection
    if db_connection:
        try:
            db_connection.close()
            print("[\033[92mOK\033[0m] Close DB Connection")
        except Exception:
            print("[\033[91mFAIL\033[0m] Close DB Connection")
            raise

def db_populate():
    global db_connection
    toy_dataset = [
        (142, "Bart", 10, 0.9),
        (123, "Milhouse", 10, 0.2),
        (857, "Lisa", 8, 0.7),
        (456, "Ralph", 8, 0.3)
    ]
    with db_connection:
        with db_connection.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    uid INTEGER PRIMARY KEY,
                    name VARCHAR(128),
                    age INTEGER,
                    pop DOUBLE PRECISION CHECK (pop >= 0 AND pop <= 1)
                )
            """)
            cur.executemany("INSERT INTO users (uid, name, age, pop) VALUES (%s, %s, %s, %s) ON CONFLICT (uid) DO NOTHING", toy_dataset)
    # db_connection.commit()

def db_clear():
    global db_connection
    with db_connection:
        with db_connection.cursor() as cur:
            cur.execute("DELETE FROM users")
    # db_connection.commit()

def db_fetch_all():
    global db_connection
    with db_connection:
        with db_connection.cursor() as cur:
            cur.execute("SELECT * FROM users ORDER BY name")
            return cur.fetchall()

def db_fetch_by_name(name):
    global db_connection
    with db_connection:
        with db_connection.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE name ILIKE %s ORDER BY uid", (f"%{name}%", ))
            return cur.fetchall()

def db_fetch_rooms(roomName, minCapacity, maxCapacity):
  
  current_datetime = datetime.now()
  print("Time right now: {}".format(current_datetime))
  
  global db_connection
  query = ('SELECT "name", "roomName", count(bo."bookEndDateTime") as bookings, "capacity", "addressLine1", '
  '"city", "province", "country", "postalCode" ')
      
  query += (
  'FROM "Building" bu '
  'JOIN "Room" r ON bu."buildingID" = r."buildingID" '
  'LEFT OUTER JOIN "Booking" bo ON bo."roomID" = r."roomID" '
  'AND bo."bookEndDateTime" > \'{}\' '
  'AND bo."bookingID" NOT IN (SELECT "bookingID" FROM "Cancellation")'
  .format(current_datetime)
  )
  
  params = []
  
  if roomName:
    query += ' AND "roomName" ILIKE %s'
    params.append(f'%{roomName}%')
  
  if minCapacity:
    query += ' AND "capacity" >= %s'
    params.append(minCapacity)
  
  if maxCapacity:
    query += ' AND "capacity" <= %s'
    params.append(maxCapacity)
  
  query += (
  ' GROUP BY '
  '"name", "roomName", "capacity", "addressLine1", '
  '"city", "province", "country", "postalCode" '
  )
  
      
  with db_connection:
    with db_connection.cursor() as cur:
      # print below for debugging purposes
      print(cur.mogrify(query, params).decode())
      cur.execute(query, params)
      return cur.fetchall()