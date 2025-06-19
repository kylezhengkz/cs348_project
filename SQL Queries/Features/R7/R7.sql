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
