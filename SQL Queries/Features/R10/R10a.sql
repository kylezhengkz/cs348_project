insert into "User" ("username", "email", "password", "permissionLevel")
values (%(userID)s, %(email)s, %(passwrd)s, 1)

returning "userID";
