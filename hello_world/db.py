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

    try:
        db_connection = psycopg2.connect(database = DB, user = DB_USERNAME, password = DB_PASSWORD, host = DB_HOST, port = DB_PORT)
        print("[\033[92mOK\033[0m] Open DB Connection")
    except Exception as e:
        db_connection = None
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



def db_fetch_rooms(roomName, minCapacity, maxCapacity, startTimeStr, endTimeStr):
  
  print(roomName, minCapacity, maxCapacity, startTimeStr, endTimeStr)
  
  use_current = True
  current_datetime = datetime.now()
  
  if startTimeStr is not None and endTimeStr is not None:
    print("DON'T USE CURRENT")
    use_current = False
    try:
      print("Attemping to parse {} and {}".format(startTimeStr, endTimeStr))
      dt_start_time = datetime.strptime(startTimeStr, "%Y-%m-%d %H:%M:%S")
      dt_end_time = datetime.strptime(endTimeStr, "%Y-%m-%d %H:%M:%S")
    except:
      print("Unable to parse date(s)")
      use_current = True
    
  print("Time right now: {}".format(current_datetime))
  
  global db_connection
  query = ('SELECT "buildingName", "roomName", count(bo."bookEndDateTime") as bookings, "capacity", "addressLine1", '
  '"city", "province", "country", "postalCode" ')
      
  query += (
  'FROM "Building" bu '
  'JOIN "Room" r ON bu."buildingID" = r."buildingID" '
  'LEFT OUTER JOIN "Booking" bo ON bo."roomID" = r."roomID" '
  'AND bo."bookingID" NOT IN (SELECT "bookingID" FROM "Cancellation") '
  )
  
  if use_current:
    query += (
    'AND (bo."bookStartDateTime" > \'{}\' '
    'OR bo."bookEndDateTime" < \'{}\') '
    .format(current_datetime, current_datetime)
    )
  else:
    query += (
    'AND (bo."bookEndDateTime" < \'{}\' '
    'OR bo."bookStartDateTime" > \'{}\') '
    .format(dt_start_time, dt_end_time)
    )
  
  params = []
  
  query += 'WHERE TRUE '
  
  if roomName:
    query += 'AND "roomName" ILIKE %s '
    params.append(f'%{roomName}%')
  
  if minCapacity:
    query += 'AND "capacity" >= %s '
    params.append(minCapacity)
  
  if maxCapacity:
    query += 'AND "capacity" <= %s '
    params.append(maxCapacity)
  
  query += (
  'GROUP BY '
  '"buildingName", "roomName", "capacity", "addressLine1", '
  '"city", "province", "country", "postalCode" '
  )
  
      
  with db_connection:
    with db_connection.cursor() as cur:
      # print below for debugging purposes
      # print(cur.mogrify(query, params).decode())
      cur.execute(query, params)
      return cur.fetchall()