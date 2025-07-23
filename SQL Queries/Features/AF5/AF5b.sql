UPDATE "User"
SET "password" = %(newPassword)s
WHERE "userID" = %(userId)s AND "password" = %(oldPassword)s;