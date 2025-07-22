export const USER_PERMS = Object.freeze({
    USER: 1,
    ADMIN: 2,
    MANAGER: 3,
});

export const USER_ROLES = {
    [USER_PERMS.USER]: "User",
    [USER_PERMS.ADMIN]: "Admin",
    [USER_PERMS.MANAGER]: "Manager",
};