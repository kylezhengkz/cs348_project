import csv
import random
import re
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time
from pathlib import Path

from ..scrapers.WebScraper import scrape_building_names

@dataclass
class Building:
    buildingID: int
    buildingName: str
    buildingPrefix: str
    addressLine1: str
    addressLine2: str
    city: str
    province: str
    country: str
    postalCode: str
    rooms: list = None

@dataclass
class Room:
    roomID: int
    roomName: str
    capacity: int
    buildingID: int
    buildingID_exists: int

@dataclass
class User:
    userID: int
    username: str
    email: str
    password: str
    permissionLevel: int

@dataclass
class Booking:
    bookingID: int
    userID: int
    roomID: int
    bookDateTime: datetime
    bookStartDateTime: datetime
    bookEndDateTime:datetime
    participants: int
    userID_exists: int
    roomID_exists: int

@dataclass
class Cancellations:
    bookingID: int
    userID: int
    cancelDateTime: datetime
    bookingID_exists: int
    userID_exists: int
    
class SampleDataGenerator:
    def __init__(self, output_dir=None, rooms_per_building=10, bookings_per_room=5, num_users=200, cancellation_rate=0.1, seed=348):
        random.seed(seed)
        self.output_dir = Path(output_dir or Path(__file__).resolve().parents[3] / "data" / "Sample Dataset")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.rooms_per_building = rooms_per_building
        self.bookings_per_room = bookings_per_room
        self.num_users = num_users
        self.cancellation_rate = max(0, min(1, cancellation_rate))
    
    def _generate_buildings(self, building_names):
        buildings = []
        for idx, building_name in enumerate(sorted(building_names), start=1):
            match = re.match(r"(.+)\s+\((\w+)\)", building_name)
            if match:
                building_prefix = match.group(2).strip()
            buildings.append(Building(
                buildingID=idx,
                buildingName=building_name,
                buildingPrefix=building_prefix,
                addressLine1="200 University Avenue West",
                addressLine2="",
                city="Waterloo",
                province="Ontario",
                country="Canada",
                postalCode="N2L 3G1"
            ))
        return buildings
    
    def _generate_rooms(self, buildings):
        room_id = 1
        for building in buildings:
            for i in range(1, self.rooms_per_building + 1):
                room_name = f"{building.buildingPrefix} {i:04}"
                capacity = random.choice([50, 100, 150, 200, 250, 300])
                room = Room(
                    roomID=room_id,
                    roomName=room_name,
                    capacity=capacity,
                    buildingID=building.buildingID,
                    buildingID_exists=0
                )
                if building.rooms is None:
                    building.rooms = []
                building.rooms.append(room)
                room_id+=1
    
    def _generate_users(self):
        first_names = ["Homer", "Marge", "Bart", "Lisa", "Sideshow", "Ned", "Apu", "Milhouse", "Maggie", "Moe", "Krusty", "Edna", "Nelson", "Barney", "Waylon", "Ralph", "Lenny", "Martin"]
        last_names = ["Prince", "Wiggum", "Simpson", "Leonard", "Skinner", "Smithers", "Gumble", "Muntz", "Krabappel", "Szyslak", "Houten", "Nahasapeemapetilon", "Flanders", "Bob", "Burns"]
        permissionLevels = [1, 2]
        
        users = []
        for user_id in range(1, self.num_users + 1):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name[0].lower()}{user_id:03}{last_name.lower()}"
            email = f"{first_name.lower()}.{last_name.lower()}@uwaterloo.ca"
            password = f"password{user_id:03}"
            permissionLevel = random.choice(permissionLevels)

            user = User(
                userID=user_id,
                username=username,
                email=email,
                password=password,
                permissionLevel=permissionLevel
            )
            users.append(user)
        return users
    
    def _generate_bookings(self, rooms, users):
        bound_start = time(7, 0, 1)
        bound_end = time(21, 59, 59)
        bookings = []
        booking_id = 1
        booking_length = timedelta(hours=1)
        base_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        base_date += timedelta(days=(7 - base_date.weekday()))

        for room in rooms:
            current_start = base_date
            for _ in range(self.bookings_per_room):
                if current_start.time() < bound_start:
                    current_start = current_start.replace(hour=19, minute=0, second=1, microsecond=0)
                if current_start.time() > bound_end:
                    current_start = current_start + timedelta(days=1)
                    current_start = current_start.replace(hour=19, minute=0, second=1, microsecond=0)
                current_end = current_start + booking_length
                user = random.choice(users)

                booking = Booking(
                    bookingID=booking_id,
                    userID=user.userID,
                    roomID=room.roomID,
                    bookDateTime=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
                    bookStartDateTime=current_start.strftime("%Y-%m-%d %I:%M:%S %p"),
                    bookEndDateTime=current_end.strftime("%Y-%m-%d %I:%M:%S %p"),
                    participants=random.randint(1, 20),
                    userID_exists=0,
                    roomID_exists=0
                )
                bookings.append(booking)
                booking_id += 1
                gap = timedelta(minutes = random.randint(5, 300))
                current_start = current_end + gap
        return bookings
    
    def _generate_cancellations(self, bookings):
        bookings_shuffled = bookings.copy()
        random.shuffle(bookings_shuffled)

        num_cancellations = self.cancellation_rate * len(bookings_shuffled)
        cancellations = []

        for booking in bookings_shuffled[:int(num_cancellations)]:
            cancellation = Cancellations(
                bookingID=booking.bookingID,
                userID=booking.userID,
                cancelDateTime=datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"),
                bookingID_exists=0,
                userID_exists=0
            )
            cancellations.append(cancellation)
        return cancellations

    def _save_buildings(self, buildings):
        filepath = self.output_dir / "Building.csv"
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "buildingID",
                "buildingName",
                "addressLine1",
                "addressLine2",
                "city",
                "province",
                "country",
                "postalCode"
            ])
            for b in buildings:
                writer.writerow([
                    b.buildingID,
                    b.buildingName,
                    b.addressLine1,
                    b.addressLine2,
                    b.city,
                    b.province,
                    b.country,
                    b.postalCode,
                ]) 
                
    def _save_rooms(self, buildings):
        filepath = self.output_dir / "Room.csv"
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "roomID",
                "roomName",
                "capacity",
                "buildingID",
                "buildingID_exists"
            ])
            for building in buildings:
                for r in building.rooms or []:
                    writer.writerow([
                        r.roomID,
                        r.roomName,
                        r.capacity,
                        r.buildingID,
                        r.buildingID_exists
                    ])
    
    def _save_users(self, users):
        filepath = self.output_dir / "User.csv"
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "userID",
                "username",
                "email",
                "password",
                "permissionLevel"
            ])
            for u in users:
                writer.writerow([
                    u.userID,
                    u.username,
                    u.email,
                    u.password,
                    u.permissionLevel
                ])
    
    def _save_bookings(self, bookings):
        filepath = self.output_dir / "Booking.csv"
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "bookingID",
                "userID",
                "roomID",
                "bookDateTime",
                "bookStartDateTime",
                "bookEndDateTime",
                "participants",
                "userID_exists",
                "roomID_exists"
            ])
            for b in bookings:
                writer.writerow([
                    b.bookingID,
                    b.userID,
                    b.roomID,
                    b.bookDateTime,
                    b.bookStartDateTime,
                    b.bookEndDateTime,
                    b.participants,
                    b.userID_exists,
                    b.roomID_exists
                ])
    
    def _save_cancellations(self, cancellations):
        filepath = self.output_dir / "Cancellation.csv"
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "bookingID",
                "userID",
                "cancelDateTime",
                "bookingID_exists",
                "userID_exists"
            ])
            for c in cancellations:
                writer.writerow([
                    c.bookingID,
                    c.userID,
                    c.cancelDateTime,
                    c.bookingID_exists,
                    c.userID_exists
                ])
    
    def generate(self):
        building_names = scrape_building_names()
        buildings = self._generate_buildings(building_names)
        users = self._generate_users()
        self._generate_rooms(buildings)

        rooms = [room for building in buildings if building.rooms for room in building.rooms]
        bookings = self._generate_bookings(rooms, users)
        cancellations = self._generate_cancellations(bookings)

        self._save_buildings(buildings)
        self._save_users(users)
        self._save_rooms(buildings)
        self._save_bookings(bookings)
        self._save_cancellations(cancellations)
