
select r."roomID", b."buildingName", r."roomName", r."capacity", b."addressLine1", b."addressLine2", b."city", b."province", b."country", b."postalCode"
from 
    "Building" as b,
    "Room" as r
WHERE (%(building_id)s IS NULL OR r."buildingID" = %(building_id)s) AND r."buildingID"=b."buildingID"
;
