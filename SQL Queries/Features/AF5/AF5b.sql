UPDATE "User"
SET "password" = %(newPassword)s
WHERE "userID" = %(userId)s;