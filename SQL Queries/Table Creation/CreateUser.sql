CREATE TABLE {UserTable} (
    "userID" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "username" TEXT,
    "email" TEXT,
    "password" TEXT,
    "permissionLevel" INT,

    PRIMARY KEY("userID"),

    CONSTRAINT validPermissionLevel CHECK ({UserTable}."permissionLevel" > 0 AND {UserTable}."permissionLevel" <= 2)
);