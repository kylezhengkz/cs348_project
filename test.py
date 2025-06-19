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

def print_all_bookings():
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
            cur.execute('SELECT * FROM "Room"')
            rows = cur.fetchall()
            if rows:
                print("\nBookings:\n")
                for row in rows:
                    print(row)
            else:
                print("No bookings found.")

        conn.close()
        print("[OK] Connection closed")
    except Exception as e:
        print("[FAIL] Error fetching bookings:", e)

if __name__ == "__main__":
    print_all_bookings()

