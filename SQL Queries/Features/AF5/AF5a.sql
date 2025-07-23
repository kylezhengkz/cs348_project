UPDATE "User"
SET "username" = %(newUsername)s
WHERE "userID" = %(userId)s;