import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta, time

from ..utils.ResourceFiles import init_resource_files, load_resource_file_data, save_to_csv_file

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

FILES = {
}

FILE_DEFAULTS = {
}

class BookingGenerator:
    def __init__(self, env, dir, rng, rooms, users, overwrite=False):
        self.env = env
        self.dir = dir
        self.overwrite = overwrite
        self.rng = rng
        self.rooms = rooms
        self.users = users
        self.csv_file = os.path.join(self.env.lower().capitalize() + ' ' + 'Dataset', 'Booking.csv')

        init_resource_files(self.dir, {'booking': self.csv_file})
        init_resource_files(self.dir, FILES, FILE_DEFAULTS, self.overwrite)
        self.data = load_resource_file_data(self.dir, FILES, FILE_DEFAULTS)
    
    def _generate_random_datetime(self, start, end):
        delta = end - start
        random_seconds = self.rng.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)

    def generate_bookings(self, num_bookings):
        initial_booking_date_min = datetime(2025, 7, 1)
        initial_booking_date_max = datetime(2025, 8, 1)

        booking_delta_seconds_min = 1
        booking_delta_seconds_max = 3 * 24 * 60 * 60

        booking_slot_seconds_min = 60 * 30
        booking_slot_seconds_max = 60 * 60 * 3

        start_booking_time_bound_min = time(7, 0, 1)
        start_booking_time_bound_max = time(22, 29, 59)

        booking_ahead_seconds_min = 60 * 3
        booking_ahead_seconds_max = 60 * 60 * 24 * 7

        bookings = []
        room_last_booking_time = {}
        user_last_booking_time = {}

        for i in range(0, num_bookings):
            room = self.rng.choice(self.rooms)
            user = self.rng.choice(self.users)

            random_initial_datetime = self._generate_random_datetime(initial_booking_date_min, initial_booking_date_max)
            earliest_candidate_booking_time = max(
                room_last_booking_time.get(room.roomID, random_initial_datetime),
                user_last_booking_time.get(user.userID, random_initial_datetime)
            )
            
            random_delta_seconds = self.rng.randint(booking_delta_seconds_min, booking_delta_seconds_max)
            start_booking_time = earliest_candidate_booking_time + timedelta(seconds=random_delta_seconds)
            if start_booking_time.time() < start_booking_time_bound_min:
                start_booking_time = start_booking_time.replace(
                    hour=start_booking_time_bound_min.hour, 
                    minute=start_booking_time_bound_min.minute,
                    second=start_booking_time_bound_min.second,
                    microsecond=start_booking_time_bound_min.microsecond
                )
            if start_booking_time.time() > start_booking_time_bound_max:
                start_booking_time = start_booking_time + timedelta(days=1)
                start_booking_time = start_booking_time.replace(
                    hour=start_booking_time_bound_min.hour, 
                    minute=start_booking_time_bound_min.minute,
                    second=start_booking_time_bound_min.second,
                    microsecond=start_booking_time_bound_min.microsecond
                )
            
            random_slot_seconds = self.rng.randint(booking_slot_seconds_min, booking_slot_seconds_max)
            end_booking_time = min(
                start_booking_time + timedelta(seconds=random_slot_seconds),
                start_booking_time.replace(
                    hour=22, 
                    minute=59,
                    second=59,
                    microsecond=0
                )
            )

            random_booking_ahead_seconds = self.rng.randint(booking_ahead_seconds_min, booking_ahead_seconds_max)
            book_date = start_booking_time - timedelta(seconds=random_booking_ahead_seconds)

            room_last_booking_time[room.roomID] = end_booking_time
            user_last_booking_time[user.userID] = end_booking_time

            bookings.append(Booking(
                bookingID=i,
                userID=user.userID,
                roomID=room.roomID,
                bookDateTime=book_date.strftime("%Y-%m-%d %I:%M:%S %p"),
                bookStartDateTime=start_booking_time.strftime("%Y-%m-%d %I:%M:%S %p"),
                bookEndDateTime=end_booking_time.strftime("%Y-%m-%d %I:%M:%S %p"),
                participants=self.rng.randint(1, 20),
                userID_exists=0,
                roomID_exists=0
            ))
        
        save_to_csv_file(
            self.dir,
            self.csv_file,
            [
                "bookingID",
                "userID",
                "roomID",
                "bookDateTime",
                "bookStartDateTime",
                "bookEndDateTime",
                "participants",
                "userID_exists",
                "roomID_exists"
            ],
            [
                [
                    b.bookingID,
                    b.userID,
                    b.roomID,
                    b.bookDateTime,
                    b.bookStartDateTime,
                    b.bookEndDateTime,
                    b.participants,
                    b.userID_exists,
                    b.roomID_exists
                ]
                for b in bookings
            ])
        return bookings

