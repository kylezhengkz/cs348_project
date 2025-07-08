import os
import secrets
import string
from dataclasses import dataclass, field

from ..utils.ResourceFiles import init_resource_files, load_resource_file_data, save_to_csv_file

@dataclass
class User:
    userID: int
    username: str
    email: str
    password: str
    permissionLevel: int

FILES = {
    'user_first_names': 'Generator Resources/users/user_first_names.txt',
    'user_last_names': 'Generator Resources/users/user_last_names.txt',
    'emails': 'Generator Resources/users/emails.txt',
    'permission_levels': 'Generator Resources/users/permission_levels.txt',
}

FILE_DEFAULTS = {
    'user_first_names': [
        'James',
        'Mary',
        'John',
        'Patricia',
        'Robert',
        'Jennifer',
        'Michael',
        'Linda',
        'William',
        'Elizabeth',
        'David',
        'Barbara',
        'Richard',
        'Susan',
        'Joseph',
        'Jessica',
        'Thomas',
        'Sarah',
        'Charles',
        'Karen',
        'Christopher',
        'Nancy',
        'Daniel',
        'Lisa',
        'Matthew',
    ],
    'user_last_names': [
        'Smith',
        'Johnson',
        'Williams',
        'Brown',
        'Jones',
        'Garcia',
        'Miller',
        'Davis',
        'Rodriguez',
        'Martinez',
        'Hernandez',
        'Lopez',
        'Gonzalez',
        'Wilson',
        'Anderson',
        'Thomas',
        'Taylor',
        'Moore',
        'Jackson',
        'Martin',
        'Lee',
        'Perez',
        'Thompson',
        'White',
        'Harris',
    ],
    'emails': [
        'yahoo.com',
        'uwaterloo.ca',
        'gmail.com',
        'proton.me',
        'outlook.ca',
    ],
    'permission_levels': ['1', '2'],
}

class UserGenerator:
    def __init__(self, env, dir, rng, overwrite=False):
        self.env = env
        self.dir = dir
        self.overwrite = overwrite
        self.rng = rng
        self.csv_file = os.path.join(self.env.lower().capitalize() + ' ' + 'Dataset', 'User.csv')

        init_resource_files(self.dir, {'user': self.csv_file})
        init_resource_files(self.dir, FILES, FILE_DEFAULTS, self.overwrite)
        self.data = load_resource_file_data(self.dir, FILES, FILE_DEFAULTS)

    def _generate_password(self, length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(characters) for _ in range(length))

    def generate_users(self, num_users):
        users = []
        used_user_names = {}

        for i in range(0, num_users):
            user_first_name = self.rng.choice(self.data['user_first_names'])
            user_last_name = self.rng.choice(self.data['user_last_names'])
            user_name = user_first_name + user_last_name
            used_user_names[user_name] = used_user_names.get(user_name, 0) + 1
            user_name = user_first_name + str(used_user_names.get(user_name, 0)) + user_last_name

            users.append(User(
                userID=i,
                username=user_name,
                email=f'{user_name}@{self.rng.choice(self.data['emails'])}',
                password=self._generate_password(),
                permissionLevel=self.rng.choice(self.data['permission_levels'])
            ))
        
        save_to_csv_file(
            self.dir,
            self.csv_file,
            [
                "userID",
                "username",
                "email",
                "password",
                "permissionLevel"
            ],
            [
                [
                    u.userID,
                    u.username,
                    u.email,
                    u.password,
                    u.permissionLevel
                ]
                for u in users
            ])
        return users

