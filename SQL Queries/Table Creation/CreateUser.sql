CREATE TABLE {UserTable} (
    "userID" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "username" TEXT UNIQUE,
    "email" TEXT UNIQUE,
    "password" TEXT,
    "permissionLevel" INT,

    PRIMARY KEY("userID"),

    CONSTRAINT validPermissionLevel CHECK ({UserTable}."permissionLevel" > 0 AND {UserTable}."permissionLevel" <= 2)
);