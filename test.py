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

def insert_user(username, eaddress, password):
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
            INSERT INTO "User" ("userID", "username", "email", "password", "permissionLevel")
            VALUES (gen_random_uuid(), %s, %s, %s, 1)
            RETURNING "userID";
            """
            cur.execute(query, (username, eaddress, password))
            user_id = cur.fetchone()[0]
            conn.commit()
            print(f"[OK] User inserted with userID: {user_id}")

        conn.close()
        print("[OK] Connection closed")
    except Exception as e:
        print("[FAIL] Error inserting user:", e)

def print_all_users():
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
            cur.execute('SELECT * FROM "User" ORDER BY "userID"')
            rows = cur.fetchall()
            if rows:
                print("\nUsers:\n")
                for row in rows:
                    print(row)
            else:
                print("No users found.")

        conn.close()
        print("[OK] Connection closed")
    except Exception as e:
        print("[FAIL] Error fetching users:", e)

def check_credentials(eaddress, password):
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
            SELECT EXISTS (
                SELECT 1 FROM "User"
                WHERE "email" = %s AND "password" = %s
            ) AS match_found;
            """
            cur.execute(query, (eaddress, password))
            result = cur.fetchone()[0]
            print(f"[OK] Credentials match: {result}")

        conn.close()
        print("[OK] Connection closed")
        return result
    except Exception as e:
        print("[FAIL] Error checking credentials:", e)
        return False

if __name__ == "__main__":
    #insert_user("Ananya O", "wrongemail@gmail.com", "wrongpass")
    print_all_users()
    check_credentials("unsafeemail@gmail.com", "unsafepass")  # Expected True
    #check_credentials("test@example.com", "wrongpass")      # Expected False