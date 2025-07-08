insert into "User" ("username", "email", "password", "permissionLevel")
values (%(username)s, %(email)s, %(passwrd)s, 1)

returning "userID";
