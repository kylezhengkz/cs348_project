INSERT INTO "Cancellation"  
(SELECT "bookingID", "userID", NOW() 
FROM "Booking"
WHERE "bookingID" = %(booking_id)s AND "userID" = %(user_id)s 
 AND "bookingID" NOT IN (SELECT "bookingID" FROM "Cancellation"));