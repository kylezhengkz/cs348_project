CREATE FUNCTION {CancellationDateTimeCheckFunc}() 
    RETURNS trigger
    LANGUAGE plpgsql AS $func$
DECLARE
    bookingCommitDateTime TIMESTAMP WITHOUT TIME ZONE;
BEGIN
    SELECT "bookDateTime" INTO bookingCommitDateTime
    FROM {BookingTable} 
    WHERE "bookingID" = NEW."bookingID";

    IF (NEW."cancelDateTime" < bookingCommitDateTime) THEN
        RAISE EXCEPTION 'The datetime for the cancellation (%) cannot be earlier than the datetime for the booking (%)', NEW."cancelDateTime", bookingCommitDateTime;
    END IF;

    RETURN NEW;
END; $func$;


CREATE TRIGGER validCancellation
BEFORE INSERT OR UPDATE ON {CancellationTable}
FOR EACH ROW
    EXECUTE FUNCTION {CancellationDateTimeCheckFunc}();