SELECT  b."bookingID",
        b."bookStartDateTime", 
        b."bookEndDateTime", 
        r."roomName",
        bl."addressLine1" || ' ' || bl."addressLine2" AS address,
        bl."buildingName", 
        bl."city", 
        bl."country"
FROM "Booking" b
JOIN "Room" r ON b."roomID" = r."roomID"
JOIN "Building" bl ON r."buildingID" = bl."buildingID"
LEFT JOIN "Cancellation" c ON b."bookingID" = c."bookingID"
WHERE b."userID" = %(user_id)s 
  AND b."bookStartDateTime" > %(now)s
  AND c."bookingID" IS NULL
ORDER BY b."bookStartDateTime";
