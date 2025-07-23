with editRoom as (
   update "Room"
   set "roomName" = %(roomName)s, "capacity" = %(capacity)s
   where "roomID" = %(roomID)s
   returning "roomID"
)


insert into "AdminEditLog"("userID", "roomID")
SELECT %(userID)s, "roomID"
FROM editRoom;