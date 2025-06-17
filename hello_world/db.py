import os
import psycopg2
import sys
from dotenv import load_dotenv
from datetime import datetime
import PyUtils as PU
import DataImporter as DI

load_dotenv()
DB = os.getenv("DATABASE")
DB_USERNAME = os.getenv("DBUSERNAME")
DB_PASSWORD = os.getenv("DBPASSWORD")
DB_HOST = os.getenv("DBHOST")
DB_PORT = os.getenv("DBPORT")

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



def db_fetch_rooms(roomName=None, minCapacity=None, maxCapacity=None, startTimeStr=None, endTimeStr=None):
  
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
  
  Secrets = PU.DBSecrets.load()
  Database = PU.DBNames.Toy.value
  importer = DI.Importer(Secrets, database = Database)
  sqlFile = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R6/R6.sql")
  sql = PU.DBTool.readSQLFile(sqlFile)
  params = {
    'room_name': f'%{roomName}%' if roomName and roomName.strip() != '' else None,
    'min_capacity': int(minCapacity) if minCapacity is not None and minCapacity.strip() != "" else None,
    'max_capacity': int(maxCapacity) if maxCapacity is not None and maxCapacity.strip() != "" else None,
    'start_time': current_datetime if use_current else dt_start_time,
    'end_time': current_datetime if use_current else dt_end_time
  }
  conn, cursor, err = importer.executeSQL(sql, vars=params, commit=True, closeConn=False)

  if (err is None):
    output = cursor.fetchall()
    conn.close()
    return output
  else:
    conn.close()


import uuid
from datetime import datetime

def db_book_room(user_id, room_id, book_date, start_time, end_time, participants):
    global db_connection
    try:
        user_uuid = uuid.UUID(user_id)
        room_uuid = uuid.UUID(room_id)
    except ValueError:
        return False, "Invalid UUID format for user ID or room ID."

    with db_connection:
        with db_connection.cursor() as cur:
            # Check if room exists
            cur.execute('SELECT 1 FROM "Room" WHERE "roomID" = %s', (str(room_uuid),))
            if not cur.fetchone():
                return False, "Room does not exist."

            # Check for overlapping bookings
            cur.execute("""
                SELECT 1 FROM "Booking"
                WHERE "roomID" = %s
                AND NOT (%s >= "bookEndDateTime" OR %s <= "bookStartDateTime")
            """, (str(room_uuid), start_time, end_time))

            if cur.fetchone():
                return False, "Room is already booked for the selected time."

            # Inserting booking
            cur.execute("""
                INSERT INTO "Booking" ("userID", "roomID", "bookDateTime", "bookStartDateTime", "bookEndDateTime", "participants")
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING "bookingID"
            """, (str(user_uuid), str(room_uuid),datetime.now(), start_time, end_time,participants))
            
            booking_id = cur.fetchone()[0]
            return True, f"Booking successful! Booking ID: {booking_id}"


def db_cancel_booking(booking_id, user_id):
    global db_connection
    try:
        booking_uuid = uuid.UUID(booking_id)
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        return False, "Invalid UUID format for booking ID or user ID."

    with db_connection:
        with db_connection.cursor() as cur:
            # Verify booking exists and belongs to the user
            cur.execute("""
                SELECT * FROM "Booking" 
                WHERE "bookingID" = %s AND "userID" = %s
            """, (str(booking_uuid), str(user_uuid)))
            booking = cur.fetchone()

            if not booking:
                return False, "Booking ID not found or does not belong to the user."

            # Insert into Cancellation table
            cur.execute("""
                INSERT INTO "Cancellation" ("bookingID", "userID", "cancelDateTime")
                VALUES (%s, %s, NOW())
            """, (str(booking_uuid), str(user_uuid)))

            # Remove from Booking table
            cur.execute("""
                DELETE FROM "Booking" 
                WHERE "bookingID" = %s
            """, (str(booking_uuid),))
            
            return True, "Booking successfully cancelled."