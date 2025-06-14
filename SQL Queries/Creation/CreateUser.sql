CREATE TABLE {UserTable} (
    "userID" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "username" TEXT,
    "email" TEXT,
    "password" TEXT,
    "permissionLevel" INT,

    PRIMARY KEY("userID")
);