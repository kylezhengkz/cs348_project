import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DB = os.getenv("DATABASE")
DB_USERNAME = os.getenv("DBUSERNAME")
DB_PASSWORD = os.getenv("DBPASSWORD")
DB_HOST = os.getenv("DBHOST")
DB_PORT = os.getenv("DBPORT")

def test_room_query():
    try:
        conn = psycopg2.connect(
            database=DB,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("[OK] Connected to database")

        with conn.cursor() as cur:
            query = """
            WITH bookingCount AS (
                SELECT 
                    r."roomID",
                    COUNT(bo."bookingID") AS "overlappingBookings"
                FROM "Room" AS r 
                LEFT OUTER JOIN "Booking" AS bo ON bo."roomID" = r."roomID"
                AND (
                    NOT EXISTS (
                        SELECT 1 
                        FROM "Cancellation" AS c
                        WHERE c."bookingID" = bo."bookingID"
                    )
                    AND NOT (
                        bo."bookStartDateTime" >= '2025-09-13 19:54:32' OR 
                        bo."bookEndDateTime" <= '2025-09-13 09:54:32'
                    )
                )
                GROUP BY r."roomID"
            )
            SELECT 
                r."roomID", 
                b."buildingName", 
                r."roomName", 
                bc."overlappingBookings", 
                r."capacity", 
                b."addressLine1", 
                b."addressLine2", 
                b."city", 
                b."province", 
                b."country", 
                b."postalCode"
            FROM bookingCount AS bc 
            JOIN "Room" AS r ON r."roomID" = bc."roomID"
            JOIN "Building" AS b ON b."buildingID" = r."buildingID"
            WHERE TRUE
                AND ('%DWB2%' IS NULL OR r."roomName" ILIKE '%DWB2%')
                AND (1 IS NULL OR r."capacity" >= 1)
                AND (1000 IS NULL OR r."capacity" <= 1000);
            """

            cur.execute(query)
            rows = cur.fetchall()
            print("\n[RESULT] Available Rooms:\n")
            for row in rows:
                print(row)

        conn.close()
        print("[OK] Connection closed")
    except Exception as e:
        print("[FAIL] Error executing room query:", e)

if __name__ == "__main__":
    test_room_query()