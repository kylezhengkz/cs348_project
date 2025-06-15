CREATE TABLE {CancellationTable} (
    "bookingID" UUID NOT NULL,
    "userID" UUID NOT NULL,
    "cancelDateTime" TIMESTAMP WITHOUT TIME ZONE,

    PRIMARY KEY ("bookingID"),
    FOREIGN KEY ("bookingID") REFERENCES {BookingTable}("bookingID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);