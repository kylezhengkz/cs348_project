INSERT INTO "Booking" VALUES (booking_id, user_id, room_id, 
date_time, start_time, end_time, participants);

UPDATE "Booking" 
SET "bookingID_exists" = 0, "userID_exists" = 0 
WHERE "bookingID" = %(booking_id)s AND "userID" = %(user_id)s;