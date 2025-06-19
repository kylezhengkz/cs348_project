import argparse
from pathlib import Path

import PyUtils as PU
import DataImporter as DI
from DataPopulator import SampleDataGenerator

def main():
    Secrets = PU.DBSecrets.load()
    Database = PU.DBNames.Dev.value
    importer = DI.Importer(Secrets, database = Database)

    parser = argparse.ArgumentParser(description="Populates database.")
    parser.add_argument("--output-dir", type=str, help="Directory to save generates CSV files.")
    parser.add_argument("--rooms-per-building", type=int, help="Number of rooms to generate per building.")
    parser.add_argument("--bookings-per-room", type=int, help="Number of bookings to generate per room.")
    parser.add_argument("--num_users", type=int, help="Number of users to generate.")
    parser.add_argument("--cancellation-rate", type=float, help="Booking cancellation rate.")
    args = parser.parse_args()

    kwargs = {}
    if args.output_dir is not None:
        kwargs["output_dir"] = args.output_dir
    if args.rooms_per_building is not None:
        kwargs["rooms_per_building"] = args.rooms_per_building
    if args.bookings_per_room is not None:
        kwargs["bookings_per_room"] = args.bookings_per_room
    if args.num_users is not None:
        kwargs["num_users"] = args.num_users
    if args.cancellation_rate is not None:
        kwargs["cancellation_rate"] = args.cancellation_rate

    print("===== GENERATING SAMPLE DATA ========")
    sg = SampleDataGenerator(**kwargs)
    sg.generate()
    print("===== SAMPLE DATA GENERATED ========")

    print("===== STARTING DATA UPLOAD ========")
    importer.importData(dataFolder=Path(PU.Paths.DataPopulatorFolder.value) / "data" / "Sample Dataset", cleanLevel=DI.ImportLevel.Tuples)
    print("===== DATA UPLOAD COMPLETE ========")


if __name__ == "__main__":
    main()
