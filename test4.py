import psycopg2
from datetime import datetime
from PyUtils import DBSecrets, DBNames
from tabulate import tabulate

# Load DB secrets
secrets = DBSecrets.load()
db_name = DBNames.Toy.value

# Booking you want to cancel
booking_id = "51d3d74c-b17b-4827-9e10-b4122dee75bf"
user_id = "24c9c44b-6a82-4022-97fe-e3b276eae7e1"

# Cancellation SQL (from r8.sql)
cancel_sql = """
INSERT INTO "Cancellation"
(SELECT "bookingID", "userID", NOW()
 FROM "Booking"
 WHERE "bookingID" = %(booking_id)s
   AND "userID" = %(user_id)s
   AND "bookingID" NOT IN (SELECT "bookingID" FROM "Cancellation"))
RETURNING "bookingID";
"""

params = {
    "booking_id": booking_id,
    "user_id": user_id
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

    # Attempt cancellation
    cur.execute(cancel_sql, params)
    row = cur.fetchone()
    conn.commit()

    if row:
        print(f"Booking {row[0]} successfully cancelled.")
    else:
        print("Cancellation failed: Already cancelled or booking/user mismatch.")

    # Show top 5 cancellations
    print("\nTop 5 recent cancellations:")
    cur.execute('SELECT * FROM "Cancellation" ORDER BY "cancelDateTime" DESC LIMIT 5')
    cancellations = cur.fetchall()
    colnames = [desc[0] for desc in cur.description]
    print(tabulate(cancellations, headers=colnames, tablefmt="pretty"))

    cur.close()
    conn.close()

except Exception as e:
    print("Error during cancellation:", e)
