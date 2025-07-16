import psycopg2
from PyUtils import DBSecrets, DBNames
import datetime
from tabulate import tabulate

def cancel_booking(booking_id, user_id):
    secrets = DBSecrets.load()
    db_name = DBNames.Toy.value  # Adjust if needed

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
                        INSERT INTO "Cancellation"  
                        (SELECT "bookingID", "userID", %(cancel_date)s
                         FROM "Booking"
                         WHERE "bookingID" = %(booking_id)s
                           AND "userID" = %(user_id)s
                           AND "bookingID" NOT IN (
                               SELECT "bookingID" FROM "Cancellation"
                           ))
                        RETURNING *;
                    """, {
                        "cancel_date": datetime.datetime.utcnow(),
                        "booking_id": booking_id,
                        "user_id": user_id
                    })

                    rows = cur.fetchall()
                    if rows:
                        col_names = [desc[0] for desc in cur.description]
                        print("[OK] Booking cancelled:")
                        print(tabulate(rows, headers=col_names, tablefmt="grid"))
                    else:
                        print("[INFO] No cancellation was made — booking may not exist or is already cancelled.")

                except Exception as e:
                    print(f"[FAIL] Cancellation failed with error: {e}")

        print("[OK] Connection closed")
    except Exception as e:
        print("[FAIL] Error connecting to database:", e)


if __name__ == "__main__":
    # Replace with actual values you want to test
    test_booking_id = "15534ebc-0051-4f19-a9dc-96b69cd63a92"
    test_user_id = "1a495a7a-434e-4439-a816-fc120955be25"
    cancel_booking(test_booking_id, test_user_id)

   # user_id="1a495a7a-434e-4439-a816-fc120955be25",
    #    room_id="99c2eb86-c61d-4cff-b5c7-41b9752f0185",
