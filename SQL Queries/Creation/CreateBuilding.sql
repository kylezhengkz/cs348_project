CREATE TABLE {BuildingTable} (
    "buildingID" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "buildingName" TEXT,
    "addressLine1" TEXT,
    "addressLine2" TEXT,
    "city" TEXT,
    "province" TEXT,
    "country" TEXT,
    "postalCode" TEXT,

    PRIMARY KEY("buildingID")
);
