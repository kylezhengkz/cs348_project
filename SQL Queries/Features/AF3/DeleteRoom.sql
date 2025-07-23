with deleteRoom as (
   delete from "Room" r
   using "Building" b
   where "roomID"=%(roomID)s and r."buildingID" = b."buildingID"
   returning "roomName", "capacity", "buildingName", "addressLine1", "addressLine2", "city", "province", "country", "postalCode"
)


insert into "AdminDeleteLog"("userID", "roomName", "capacity", "buildingName", "addressLine1", "addressLine2", "city", "province", "country", "postalCode")
SELECT %(userID)s, "roomName", "capacity", "buildingName", "addressLine1", "addressLine2", "city", "province", "country", "postalCode"
FROM deleteRoom;
