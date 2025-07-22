WITH 
    cancelledBookingIDs AS (
        SELECT
            C."bookingID"
        FROM (SELECT "bookingID" FROM "Booking" B1 WHERE B1."userID" = %(userId)s) B
        JOIN "Cancellation" C
            ON B."bookingID" = C."bookingID"
    ),

    targetUser AS (
        SELECT U1."userID" FROM "User" U1 WHERE U1."userID" = %(userId)s
    ),

    availableBookings AS (
        SELECT 
            B1."roomID", 
            B1."userID",
            R."roomName"
        FROM (SELECT R1."roomID", R1."roomName" FROM "Room" R1) R
        JOIN "Booking" B1
            ON B1."roomID" = R."roomID"
        WHERE B1."userID" = %(userId)s AND
              B1."bookingID" NOT IN (SELECT * FROM cancelledBookingIDs) AND
              (%(startDateTime)s IS NULL OR B1."bookEndDateTime" >= %(startDateTime)s) AND
              (%(endDateTime)s IS NULL OR B1."bookStartDateTime" <= %(endDateTime)s)
    )

SELECT
    B."roomID",
    B."roomName",
    COUNT(*) AS "bookingCount"
FROM targetUser U
JOIN availableBookings B
    ON B."userID" = U."userID"
GROUP BY B."roomID", B."roomName"
ORDER BY "bookingCount" DESC, B."roomID";