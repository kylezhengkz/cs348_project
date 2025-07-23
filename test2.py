import os
import psycopg2
import uuid
from datetime import datetime
from dotenv import load_dotenv
from PyUtils import DBSecrets, DBNames
from tabulate import tabulate

# Load DB secrets
secrets = DBSecrets.load()
db_name = DBNames.Toy.value

# Booking test data
#user_id = "0ccdb479-09e3-47f8-9b3e-39436d041848"
#room_id = "03b6ba76-b397-4386-a405-f39dca0e86cb"
user_id = '24c9c44b-6a82-4022-97fe-e3b276eae7e1'
room_id = '9a1c48f9-c9d9-4a06-9a29-912caecd8288'
book_date = "2025-11-22"
start_time_str = "15:36"
end_time_str = "16:10"
participants = 9

# Parse times
try:
    start_time = datetime.strptime(f"{book_date} {start_time_str}", "%Y-%m-%d %H:%M")
    end_time = datetime.strptime(f"{book_date} {end_time_str}", "%Y-%m-%d %H:%M")
except ValueError as e:
    print("Date parsing error:", e)
    exit(1)

book_datetime = datetime.now()

# SQL from from R7.sql
booking_sql = """
WITH valid_room AS (
    SELECT 1 FROM "Room" WHERE "roomID" = %(roomID)s
),
valid_booking AS (
    SELECT 1
    FROM "Booking" AS b
    WHERE b."roomID" = %(roomID)s
      AND NOT EXISTS (
          SELECT 1 FROM "Cancellation" AS c
          WHERE c."bookingID" = b."bookingID"
      )
      AND NOT (
          %(startTime)s >= b."bookEndDateTime"
          OR %(endTime)s <= b."bookStartDateTime"
      )
)
INSERT INTO "Booking" (
    "userID", "roomID", "bookDateTime",
    "bookStartDateTime", "bookEndDateTime", "participants"
)
SELECT
    %(userID)s, %(roomID)s, %(bookDateTime)s,
    %(startTime)s, %(endTime)s, %(participants)s
WHERE EXISTS (SELECT 1 FROM valid_room)
  AND NOT EXISTS (SELECT 1 FROM valid_booking)
RETURNING "bookingID";
"""

params = {
    "userID": user_id,
    "roomID": room_id,
    "bookDateTime": datetime.now(),
    "startTime": start_time,
    "endTime": end_time,
    "participants": participants
}

try:
    conn = psycopg2.connect(
        database=db_name,
        user=secrets.username,
        password=secrets.password,
        host=secrets.host,
        port=secrets.port
    )
    cur = conn.cursor()
    cur.execute(booking_sql, params)
    row = cur.fetchone()
    conn.commit()

    if row:
        print("Booking successful! Booking ID:", row[0])
    else:
        print("Booking failed: room does not exist or is already booked.")

    print("\n📋 Top 5 recent bookings:")
    cur.execute("""SELECT * FROM "Booking" where "userID" ='24c9c44b-6a82-4022-97fe-e3b276eae7e1' ORDER BY "bookDateTime" DESC LIMIT 5""")
    bookings = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    print(tabulate(bookings, headers=colnames, tablefmt="pretty"))

    cur.close()
    conn.close()

except Exception as e:
    print("Error during booking:", e)
