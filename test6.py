import psycopg2
from PyUtils import DBSecrets, DBNames
import datetime
from tabulate import tabulate

def view_upcoming_bookings(user_id):
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

        with conn.cursor() as cur:
            try:
                cur.execute("""
                    SELECT  
                        b."bookingID",
                        b."bookStartDateTime", 
                        b."bookEndDateTime", 
                        r."roomName",
                        bl."addressLine1" || ' ' || bl."addressLine2" AS address,
                        bl."buildingName", 
                        bl."city", 
                        bl."country"
                    FROM "Booking" b
                    JOIN "Room" r ON b."roomID" = r."roomID"
                    JOIN "Building" bl ON r."buildingID" = bl."buildingID"
                    LEFT JOIN "Cancellation" c ON b."bookingID" = c."bookingID"
                    WHERE b."userID" = %(user_id)s 
                      AND b."bookStartDateTime" > %(now)s
                      AND c."bookingID" IS NULL
                    ORDER BY b."bookStartDateTime";
                """, {
                    "user_id": user_id,
                    "now": datetime.datetime.utcnow()
                })

                rows = cur.fetchall()
                if rows:
                    col_names = [desc[0] for desc in cur.description]
                    print("[OK] Upcoming bookings:")
                    print(tabulate(rows, headers=col_names, tablefmt="grid"))
                else:
                    print("[INFO] No upcoming bookings found for this user.")

            except Exception as e:
                print(f"[FAIL] Query failed with error: {e}")

        conn.close()
        print("[OK] Connection closed")
    except Exception as e:
        print("[FAIL] Error connecting to database:", e)

if __name__ == "__main__":
    # Example user ID — replace with real one as needed
    view_upcoming_bookings("d9503ce7-58fb-4eff-a914-59adac8fa864")
