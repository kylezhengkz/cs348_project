CREATE TABLE {BookingTable} (
    "bookingID" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "userID" UUID NOT NULL,
    "roomID" UUID NOT NULL,
    "bookDateTime" TIMESTAMP WITHOUT TIME ZONE,
    "bookStartDateTime" TIMESTAMP WITHOUT TIME ZONE,
    "bookEndDateTime" TIMESTAMP WITHOUT TIME ZONE,
    "participants" INT,

    PRIMARY KEY("bookingID"),
    FOREIGN KEY("userID") REFERENCES {UserTable}("userID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY("roomID") REFERENCES {RoomTable}("roomID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
);