SELECT
    bu."buildingName",
    r."roomName",
    r."capacity",
    bu."addressLine1",
    bu."city",
    bu."province",
    bu."country",
    bu."postalCode"
FROM "Room" AS r
JOIN "Building" AS bu ON bu."buildingID" = r."buildingID"
WHERE TRUE
    AND (%(room_name)s IS NULL OR r."roomName" ILIKE %(room_name)s)
    AND (%(min_capacity)s IS NULL OR r."capacity" >= %(min_capacity)s)
    AND (%(max_capacity)s IS NULL OR r."capacity" <= %(max_capacity)s)
    AND NOT EXISTS (
        SELECT 1
        FROM "Booking" AS bo
        LEFT JOIN "Cancellation" AS c ON bo."bookingID" = c."bookingID"
        WHERE bo."roomID" = r."roomID"
            AND c."bookingID" IS NULL
            AND bo."bookStartDateTime" < %(end_time)s
            AND bo."bookEndDateTime" > %(start_time)s
    )
GROUP BY
    bu."buildingName",
    r."roomName",
    r."capacity",
    bu."addressLine1",
    bu."city",
    bu."province",
    bu."country",
    bu."postalCode";