import os
from dataclasses import dataclass, field

from ..utils.ResourceFiles import init_resource_files, load_resource_file_data, save_to_csv_file

@dataclass
class Room:
    roomID: int
    roomName: str
    capacity: int
    buildingID: int
    buildingID_exists: int

FILES = {
    'room_capacities': 'Generator Resources/rooms/room_capacity.txt',
}

FILE_DEFAULTS = {
    'room_capacities': ['25', '50', '75', '100', '125', '150', '175', '200'],
}

class RoomGenerator:
    def __init__(self, env, dir, rng, buildings, overwrite=False):
        self.env = env
        self.dir = dir
        self.overwrite = overwrite
        self.rng = rng
        self.buildings = buildings
        self.csv_file = os.path.join(self.env.lower().capitalize() + ' ' + 'Dataset', 'Room.csv')

        init_resource_files(self.dir, {'room': self.csv_file})
        init_resource_files(self.dir, FILES, FILE_DEFAULTS, self.overwrite)
        self.data = load_resource_file_data(self.dir, FILES, FILE_DEFAULTS)
    
    def generate_rooms(self, num_rooms):
        rooms = []
        used_room_names = {}

        for i in range(0, num_rooms):
            building = self.rng.choice(self.buildings)
            room_name = f'{building.buildingTag}'
            used_room_names[room_name] = used_room_names.get(room_name, 0) + 1
            room_name = room_name + ' ' + str(used_room_names.get(room_name, 0))

            rooms.append(Room(
                roomID=i,
                roomName=room_name,
                capacity=self.rng.choice(self.data['room_capacities']),
                buildingID=building.buildingID,
                buildingID_exists=0
            ))
        
        save_to_csv_file(
            self.dir,
            self.csv_file,
            [
                "roomID",
                "roomName",
                "capacity",
                "buildingID",
                "buildingID_exists"
            ],
            [
                [
                    r.roomID,
                    r.roomName,
                    r.capacity,
                    r.buildingID,
                    r.buildingID_exists
                ]
                for r in rooms
            ])
        return rooms

