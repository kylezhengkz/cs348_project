import random
from pathlib import Path

import PyUtils as PU
import DataImporter as DI
from DataPopulator.utils.CmdlHandler import parse_args, summarize_args, confirm_or_exit
from DataPopulator.data_generators.BuildingGenerator import BuildingGenerator
from DataPopulator.data_generators.RoomGenerator import RoomGenerator
from DataPopulator.data_generators.UserGenerator import UserGenerator
from DataPopulator.data_generators.BookingGenerator import BookingGenerator
from DataPopulator.data_generators.CancellationGenerator import CancellationGenerator
from DataPopulator.utils.CmdMessages import print_header

def main():
    args = parse_args()
    summarize_args(args)
    confirm_or_exit()

    Secrets = PU.DBSecrets.load()
    Database = args.environment
    importer = DI.Importer(Secrets, database = Database)
    
    rng = random.Random(args.random_seed) if args.random_seed is not None else random.Random()

    if args.scrape:
        print_header('INIT: WEB SCRAPING')
        print_header('DONE: WEB SCRAPING')
    if args.generate:
        print_header('INIT: GENERATE DATASET')
        
        bug = BuildingGenerator(args.environment, args.directory, rng, args.overwrite)
        buildings = bug.generate_buildings(args.num_buildings)
        
        rog = RoomGenerator(args.environment, args.directory, rng, buildings, args.overwrite)
        rooms = rog.generate_rooms(args.num_rooms)

        usg = UserGenerator(args.environment, args.directory, rng, args.overwrite)
        users = usg.generate_users(args.num_users)

        bog = BookingGenerator(args.environment, args.directory, rng, rooms, users, args.overwrite)
        bookings = bog.generate_bookings(args.num_bookings)

        cag = CancellationGenerator(args.environment, args.directory, rng, bookings, args.overwrite)
        cancellations = cag.generate_cancellations(args.num_cancellations)

        print_header('DONE: GENERATE DATASET')
    if args.populate:
        print_header('INIT: POPULATE DATABASE')

        importer.importData(dataFolder=Path(PU.Paths.DataFolder.value) / f'{args.environment.lower().capitalize()} Dataset', cleanLevel=DI.ImportLevel.Tuples)

        print_header('DONE: POPULATE DATABASE')

if __name__ == "__main__":
    main()
