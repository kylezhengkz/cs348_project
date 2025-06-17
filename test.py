import uuid
from datetime import datetime
from hello_world.db import db_open_connection, db_close_connection, db_book_room
import psycopg2

# Open the DB connection
db_open_connection()

# test values
user_id = "98b2e476-7929-4dc8-aebd-e782c4ad0f39"
room_id = "fea78062-118e-4720-aa73-ddfe9a3cc6a3"
book_date = "2025-09-29"
start_time = "09:35"
end_time = "11:35"
participants = 2

start_datetime = datetime.strptime(f"{book_date} {start_time}", "%Y-%m-%d %H:%M")
end_datetime = datetime.strptime(f"{book_date} {end_time}", "%Y-%m-%d %H:%M")

# Booking the room
success, message = db_book_room(user_id, room_id, book_date, start_datetime, end_datetime, participants)

# Booking results
print("Success:", success)
print("Message:", message)

# Printing booking table content to check if booking is there
from hello_world.db import db_connection
with db_connection:
    with db_connection.cursor() as cur:
        print("\nCurrent records in Booking table:")
        cur.execute('SELECT * FROM "Booking" ORDER BY "bookStartDateTime" DESC')
        rows = cur.fetchall()
        for row in rows:
            print(row)

# Close connection
db_close_connection()
