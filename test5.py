import psycopg2
from PyUtils import DBSecrets, DBNames
import datetime
from tabulate import tabulate

def try_insert_booking(user_id, room_id, start_time, end_time, participants):
    secrets = DBSecrets.load()
    db_name = DBNames.Toy.value  # Update if needed

    try:
        conn = psycopg2.connect(
            database='production',
            user=secrets.username,
            password=secrets.password,
            host=secrets.host,
            port=secrets.port
        )
        print("[OK] Connected to database")

        with conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("""
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
                        RETURNING *;
                    """, {
                        "userID": user_id,
                        "roomID": room_id,
                        "bookDateTime": datetime.datetime.utcnow(),
                        "startTime": start_time,
                        "endTime": end_time,
                        "participants": participants
                    })

                    rows = cur.fetchall()
                    if rows:
                        col_names = [desc[0] for desc in cur.description]
                        print("[OK] Booking successful:")
                        print(tabulate(rows, headers=col_names, tablefmt="grid"))
                    else:
                        print("[INFO] Booking not created — likely due to conflict or invalid room.")

                except Exception as e:
                    print(f"[FAIL] Booking insert failed with error: {e}")

        print("[OK] Connection closed")
    except Exception as e:
        print("[FAIL] Error connecting to database:", e)

if __name__ == "__main__":
    # Example test case
    try_insert_booking(
        user_id="1a495a7a-434e-4439-a816-fc120955be25",
        room_id="99c2eb86-c61d-4cff-b5c7-41b9752f0185",
        start_time=datetime.datetime(2025, 7, 15, 10, 0),
        end_time=datetime.datetime(2025, 7, 15, 11, 0),
        participants=3
    )


