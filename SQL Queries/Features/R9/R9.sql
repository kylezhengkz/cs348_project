SELECT
   b."bookingID",
   b."userID",
   b."roomID",
   b."bookDateTime",
   b."bookStartDateTime",
   b."bookEndDateTime",
   b."participants",
   r."roomName",
   bl."buildingName",
   bl."addressLine1" || ' ' || COALESCE(bl."addressLine2", '') AS address,
   bl."city",
   bl."country",
   CASE
       WHEN c."bookingID" IS NOT NULL THEN TRUE
       ELSE FALSE
   END AS cancelled
FROM "Booking" b
JOIN "Room" r ON b."roomID" = r."roomID"
JOIN "Building" bl ON r."buildingID" = bl."buildingID"
LEFT JOIN "Cancellation" c ON b."bookingID" = c."bookingID"
WHERE b."userID" = %(user_id)s
ORDER BY b."bookDateTime" DESC;