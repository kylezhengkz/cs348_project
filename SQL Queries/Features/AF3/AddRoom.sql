with newRoom as (
   insert into "Room"("roomName", "capacity", "buildingID")
   values (%(roomName)s, %(capacity)s, %(buildingID)s)
   returning "roomID"
)


insert into "AdminAddLog"("userID", "roomID")
SELECT %(userID)s, "roomID"
FROM newRoom;
