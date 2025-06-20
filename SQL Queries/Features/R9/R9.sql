SELECT
   b."bookingID",
   b."userID",
   b."roomID",
   b."bookDateTime",
   b."bookStartDateTime",
   b."bookEndDateTime",
   b."participants",
   CASE
       WHEN c."bookingID" IS NOT NULL THEN TRUE
       ELSE FALSE
   END AS cancelled
FROM "Booking" b
LEFT JOIN "Cancellation" c ON b."bookingID" = c."bookingID"
WHERE b."userID" = %(userID)s
ORDER BY b."bookDateTime" DESC;