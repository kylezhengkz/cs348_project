CREATE VIEW "AdminLogsView" AS
SELECT
  a."logID",
  a."userID",
  a."roomID",
  r."roomName",
  r."capacity",
  b."buildingName",
  b."addressLine1",
  b."addressLine2",
  b."city",
  b."province",
  b."country",
  b."postalCode",
  'add' AS "action"
FROM "AdminAddLog" a
JOIN "Room" r ON a."roomID" = r."roomID"
JOIN "Building" b ON r."buildingID" = b."buildingID"

UNION ALL

SELECT
  e."logID",
  e."userID",
  e."roomID",
  r."roomName",
  r."capacity",
  b."buildingName",
  b."addressLine1",
  b."addressLine2",
  b."city",
  b."province",
  b."country",
  b."postalCode",
  'edit' AS "action"
FROM "AdminEditLog" e
JOIN "Room" r ON e."roomID" = r."roomID"
JOIN "Building" b ON r."buildingID" = b."buildingID"

UNION ALL

SELECT
  d."logID",
  d."userID",
  NULL AS "roomID",
  d."roomName",
  d."capacity",
  d."buildingName",
  d."addressLine1",
  d."addressLine2",
  d."city",
  d."province",
  d."country",
  d."postalCode",
  'delete' AS "action"
FROM "AdminDeleteLog" d;
