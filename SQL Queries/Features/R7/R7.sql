INSERT INTO "Booking" ("userID", "roomID", "bookDateTime", "bookStartDateTime", "bookEndDateTime", "participants")
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING "bookingID";