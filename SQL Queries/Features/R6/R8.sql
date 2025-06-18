INSERT INTO "Cancellation"  
(SELECT "bookingID", "userID", NOW() 
FROM "Booking"
WHERE "bookingID" = %(booking_id)s AND "userID" = %(user_id)s 
 AND "bookingID" NOT IN (SELECT "bookingID" FROM "Cancellation"));

UPDATE "Cancellation" 
SET "bookingID_exists" = 0, "userID_exists" = 0 
WHERE "bookingID" = %(booking_id)s AND "userID" = %(user_id)s;