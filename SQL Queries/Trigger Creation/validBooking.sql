CREATE FUNCTION {BookingParticipantsCheckFunc}() 
    RETURNS trigger
    LANGUAGE plpgsql AS $func$ 
DECLARE
    roomCapacity INT;
BEGIN
    SELECT "capacity" INTO roomCapacity
    FROM {RoomTable} 
    WHERE "roomID" = NEW."roomID";

    IF (NEW."participants" > roomCapacity) THEN
        RAISE EXCEPTION 'The number of participants in the booking (%) is not smaller or equal to the capacity of the room (%)', NEW."participants", roomCapacity;
    END IF;

    RETURN NEW;
END; $func$;


CREATE TRIGGER validBooking
BEFORE INSERT OR UPDATE ON {BookingTable}
FOR EACH ROW
    EXECUTE FUNCTION {BookingParticipantsCheckFunc}();