-- maps each roomID to number of booked participants that overlap with [start_time, end_time]
with bookingCount as (
  select 
  	r."roomID",
	  count(bo."bookingID") as "overlappingBookings"
  from "Room" as r 
  left outer join "Booking" as bo 
    on bo."roomID" = r."roomID"
  and (
	  not exists ( -- disregard cancelled bookings and join bookings that overlap with [start_time, end_time]
		select 1 
		from "Cancellation" as c
		where c."bookingID" = bo."bookingID" -- cancelled
	  )
	  and not (bo."bookStartDateTime" >= %(end_time)s or bo."bookEndDateTime" <= %(start_time)s) -- overlap
  )
  group by r."roomID"
)


-- display the appropriate columns to the view rooms
select r."roomID", b."buildingName", r."roomName", bc."overlappingBookings", r."capacity", b."addressLine1", b."addressLine2", b."city", b."province", b."country", b."postalCode"
from bookingCount as bc 
join "Room" as r on r."roomID" = bc."roomID"
join "Building" as b on b."buildingID" = r."buildingID"
WHERE TRUE
    AND (%(room_name)s IS NULL OR r."roomName" ILIKE %(room_name)s)
    AND (%(min_capacity)s IS NULL OR r."capacity" >= %(min_capacity)s)
    AND (%(max_capacity)s IS NULL OR r."capacity" <= %(max_capacity)s);
