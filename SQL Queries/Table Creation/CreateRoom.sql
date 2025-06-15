CREATE TABLE {RoomTable} (
    "roomID" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "roomName" TEXT,
    "buildingID" UUID NOT NULL,
    "capacity" INT,

    PRIMARY KEY("roomID"),
    FOREIGN KEY("buildingID") REFERENCES {BuildingTable}("buildingID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    CONSTRAINT validCapacity CHECK ({RoomTable}."capacity" > 0)
);