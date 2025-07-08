import os
from datetime import datetime, timedelta, time
from dataclasses import dataclass, field

from ..utils.ResourceFiles import init_resource_files, load_resource_file_data, save_to_csv_file

@dataclass
class Cancellation:
    bookingID: int
    userID: int
    cancelDateTime: datetime
    bookingID_exists: int
    userID_exists: int

FILES = {
}

FILE_DEFAULTS = {
}

class CancellationGenerator:
    def __init__(self, env, dir, rng, bookings, overwrite=False):
        self.env = env
        self.dir = dir
        self.overwrite = overwrite
        self.rng = rng
        self.bookings = bookings
        self.csv_file = os.path.join(self.env.lower().capitalize() + ' ' + 'Dataset', 'Cancellation.csv')

        init_resource_files(self.dir, {'cancellations': self.csv_file})
        init_resource_files(self.dir, FILES, FILE_DEFAULTS, self.overwrite)
        self.data = load_resource_file_data(self.dir, FILES, FILE_DEFAULTS)
    
    def _generate_random_datetime(self, start, end):
        delta = end - start
        random_seconds = self.rng.randint(0, int(delta.total_seconds()))
        return start + timedelta(seconds=random_seconds)

    def generate_cancellations(self, num_cancellations):
        cancellations = []

        for i in range(0, num_cancellations):
            booking = self.rng.choice(self.bookings)
            self.bookings.remove(booking)

            cancellations.append(Cancellation(
                bookingID=booking.bookingID,
                userID=booking.userID,
                cancelDateTime=self._generate_random_datetime(
                    datetime.strptime(booking.bookDateTime, "%Y-%m-%d %I:%M:%S %p"), 
                    datetime.strptime(booking.bookStartDateTime, "%Y-%m-%d %I:%M:%S %p")
                ).strftime("%Y-%m-%d %I:%M:%S %p"),
                bookingID_exists=0,
                userID_exists=0
            ))
        
        save_to_csv_file(
            self.dir,
            self.csv_file,
            [
                "bookingID",
                "userID",
                "cancelDateTime",
                "bookingID_exists",
                "userID_exists"
            ],
            [
                [
                    c.bookingID,
                    c.userID,
                    c.cancelDateTime,
                    c.bookingID_exists,
                    c.userID_exists
                ]
                for c in cancellations
            ])
        return cancellations

