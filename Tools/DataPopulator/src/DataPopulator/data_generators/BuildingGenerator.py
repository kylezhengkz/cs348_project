import os
from dataclasses import dataclass, field

from ..utils.ResourceFiles import init_resource_files, load_resource_file_data, save_to_csv_file

@dataclass
class Building:
    buildingID: int
    buildingName: str
    buildingTag: str
    addressLine1: str
    addressLine2: str
    city: str
    province: str
    country: str
    postalCode: str
    rooms: list = None

FILES = {
    'building_name_prefix': 'Generator Resources/buildings/building_name_prefix.txt',
    'building_name_suffix': 'Generator Resources/buildings/building_name_suffix.txt',
    'street_names': 'Generator Resources/buildings/street_names.txt',
    'street_types': 'Generator Resources/buildings/street_types.txt', 
    'directional_prefixes': 'Generator Resources/buildings/directional_prefixes.txt', 
    'cities': 'Generator Resources/buildings/cities.txt', 
}

FILE_DEFAULTS = {
    'building_name_prefix': ['Architecture', 'Engineering', 'Chemistry', 'Math', 'Health', 'Arts', 'Science', 'Pharmacy', 'Minota Hagey', 'Dana Porter', 'Columbia Lake', 'Douglas Wright', 'Federation', 'Claudette Millar', 'Ira G. Needles', 'Carl A. Pollock', 'Virginia Woolf', 'Margaret Atwood', 'Jane Austen'],
    'building_name_suffix': ['Arena', 'Building', 'Residence', 'Library', 'Campus', 'Village', 'Services', 'Hall', 'Garage', 'Lecture Hall', 'Center', 'North Block', 'East Block', 'South Block', 'West Block'],
    'street_names': ['University', 'Philips', 'King', 'Queen', 'Main'],
    'street_types': ['St', 'Ave', 'Blvd', 'Rd', 'Ln'],
    'directional_prefixes': ['N', 'S', 'E', 'W', ''],
    'cities': ['Toronto', 'Waterloo', 'Kitchener', 'Mississauga', 'Vaughan', 'Hamilton', 'Windsor', 'Oshawa', 'Brampton', 'Ottawa', 'Sudbury'],
}

class BuildingGenerator:
    def __init__(self, env, dir, rng, overwrite=False):
        self.env = env
        self.dir = dir
        self.overwrite = overwrite
        self.rng = rng
        self.csv_file = os.path.join(self.env.lower().capitalize() + ' ' + 'Dataset', 'Building.csv')

        init_resource_files(self.dir, {'building': self.csv_file})
        init_resource_files(self.dir, FILES, FILE_DEFAULTS, self.overwrite)
        self.data = load_resource_file_data(self.dir, FILES, FILE_DEFAULTS)
    
    def _generate_postal_code(self):
        # HARDCODED ONTARIO
        valid_ontario_first_letters = 'KLMNP'
        valid_letters = 'ABCEGHJKLMNPRSTVXY'
        return (
            self.rng.choice(valid_ontario_first_letters) +
            str(self.rng.randint(0, 9)) +
            self.rng.choice(valid_letters) +
            ' ' +
            str(self.rng.randint(0, 9)) +
            self.rng.choice(valid_letters) +
            str(self.rng.randint(0, 9))
        )
    
    def generate_buildings(self, num_buildings):
        buildings = []
        used_building_names = {}

        for i in range(0, num_buildings):
            building_name = f"{self.rng.choice(self.data['building_name_prefix'])} {self.rng.choice(self.data['building_name_suffix'])}"
            used_building_names[building_name] = used_building_names.get(building_name, 0) + 1
            building_name = building_name + ' ' + str(used_building_names.get(building_name, 0))
            building_tag = ''.join(word[0] for word in building_name.split())

            buildings.append(Building(
                buildingID=i,
                buildingName=building_name,
                buildingTag=building_tag,
                addressLine1=f"{self.rng.randint(100, 999)} {self.rng.choice(self.data['street_names'])} {self.rng.choice(self.data['street_types'])} {self.rng.choice(self.data['directional_prefixes'])}",
                addressLine2='',
                city=f"{self.rng.choice(self.data['cities'])}",
                # HARDCODED ONTARIO CANADA
                province='Ontario',
                country='Canada',
                postalCode=f'{self._generate_postal_code()}'
            ))
        
        save_to_csv_file(
            self.dir,
            self.csv_file,
            [
                "buildingID",
                "buildingName",
                "addressLine1",
                "addressLine2",
                "city",
                "province",
                "country",
                "postalCode"
            ],
            [
                [
                    b.buildingID,
                    b.buildingName,
                    b.addressLine1,
                    b.addressLine2,
                    b.city,
                    b.province,
                    b.country,
                    b.postalCode,
                ]
                for b in buildings
            ])
        return buildings

