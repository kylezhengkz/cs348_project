-- maps each roomID to number of booked participants that overlap with [start_time, end_time]
with bookingCount as (
  select 
  	r."roomID",
	sum(bo."participants") as "bookingNum"
  from "Room" as r 
  left outer join "Booking" as bo on bo."roomID" = r."roomID"
  and (
	  not exists ( -- disregard cancalled bookings and bookings that do not overlap with [start_time, end_time]
		select 1 
		from "Cancellation" as c
		where c."bookingID" = bo."bookingID" -- cancelled
			or (bo."bookStartDateTime" >= %(end_time)s or bo."bookEndDateTime" <= %(start_time)s) -- overlap
	  )
  )
  group by r."roomID"
)


-- display the appropriate columns to the view rooms
select r."roomID", b."buildingName", r."roomName", bc."bookingNum", r."capacity", b."addressLine1", b."city", b."province", b."country", b."postalCode"
from bookingCount as bc 
join "Room" as r on r."roomID" = bc."roomID"
join "Building" as b on b."buildingID" = r."buildingID"
;
