create table "AdminAddLog" (
	"logID" UUID NOT NULL DEFAULT uuid_generate_v4(),
	"userID" UUID NOT NULL,
	"roomID" UUID NOT NULL,
	
	PRIMARY KEY("logID"),

	FOREIGN KEY("userID") REFERENCES "User"("userID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,

	FOREIGN KEY("roomID") REFERENCES "Room"("roomID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
;

create table "AdminEditLog" (
	"logID" UUID NOT NULL DEFAULT uuid_generate_v4(),
	"userID" UUID NOT NULL,
	"roomID" UUID NOT NULL,
	
	PRIMARY KEY("logID"),

	FOREIGN KEY("userID") REFERENCES "User"("userID")
        ON DELETE CASCADE
        ON UPDATE CASCADE,

	FOREIGN KEY("roomID") REFERENCES "Room"("roomID")
        ON DELETE CASCADE
        ON UPDATE CASCADE
)
;

create table "AdminDeleteLog" (
	"logID" UUID NOT NULL DEFAULT uuid_generate_v4(),
	"userID" UUID NOT NULL,
	"roomName" TEXT,
    "capacity" INT,
	"buildingName" TEXT NOT NULL,
    "addressLine1" TEXT NOT NULL,
    "addressLine2" TEXT NOT NULL,
    "city" TEXT NOT NULL,
    "province" TEXT NOT NULL,
    "country" TEXT NOT NULL,
    "postalCode" TEXT NOT NULL,

	PRIMARY KEY("logID"),

	FOREIGN KEY("userID") REFERENCES "User"("userID")
)
;

CREATE OR REPLACE FUNCTION admins_only()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM "User" u
    WHERE u."userID" = NEW."userID" AND u."permissionLevel" = 1
  ) THEN
    RAISE EXCEPTION 'Non-admin attempted to execute restricted query';
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER "CheckAdminBeforeInsert_Add"
BEFORE INSERT ON "AdminAddLog"
FOR EACH ROW
EXECUTE FUNCTION admins_only();

CREATE TRIGGER "CheckAdminBeforeInsert_Edit"
BEFORE INSERT ON "AdminEditLog"
FOR EACH ROW
EXECUTE FUNCTION admins_only();

CREATE TRIGGER "CheckAdminBeforeInsert_Delete"
BEFORE INSERT ON "AdminDeleteLog"
FOR EACH ROW
EXECUTE FUNCTION admins_only();
