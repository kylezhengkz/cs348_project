CREATE TABLE {BuildingTable} (
    "buildingID" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "buildingName" TEXT NOT NULL,
    "addressLine1" TEXT NOT NULL,
    "addressLine2" TEXT NOT NULL,
    "city" TEXT NOT NULL,
    "province" TEXT NOT NULL,
    "country" TEXT NOT NULL,
    "postalCode" TEXT NOT NULL,

    PRIMARY KEY("buildingID"),
    UNIQUE("buildingName", "addressLine1", "addressLine2", "city", "province", "country", "postalCode")
);
