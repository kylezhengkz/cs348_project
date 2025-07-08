import argparse
import os
import sys
from pathlib import Path

import PyUtils as PU

# --- Individual argument validation ---
def _positive_int(val):
    int_val = int(val)
    if int_val <= 0:
        raise argparse.ArgumentTypeError(f'{val} is not a positive integer')
    return int_val

def _non_negative_int(val):
    int_val = int(val)
    if int_val < 0:
        raise argparse.ArgumentTypeError(f'{val} is not a non-negative integer')
    return int_val

def _dir_path(val):
    path_val = Path(val)
    if not path_val.exists():
        raise argparse.ArgumentTypeError(f'directory does not exist: {val}')
    if not path_val.is_dir():
        raise argparse.ArgumentTypeError(f'Not a directory: {val}')
    if not os.access(path_val, os.R_OK | os.W_OK):
        raise argparse.ArgumentTypeError(f'No read/write permissions for directory: {val}')
    
    for subpath in path_val.rglob('*'):
        if subpath.is_dir():
            if not os.access(path_val, os.R_OK | os.W_OK):
                raise argparse.ArgumentTypeError(f'No read/write permissions for subdirectory: {subpath}')
        elif subpath.is_file():
            if not os.access(path_val, os.R_OK | os.W_OK):
                raise argparse.ArgumentTypeError(f'No read/write permissions for file: {subpath}')
    return path_val

def _database_env(val):
    str_val = str(val).lower()
    env_val = None

    if str_val == 'toy':
        env_val = PU.DBNames.Toy.value
    elif str_val == 'dev':
        env_val = PU.DBNames.Dev.value
    elif str_val == 'prod':
        env_val = PU.DBNames.Prod.value
    elif str_val == 'toyunittest':
        env_val = PU.DBNames.ToyUnitTest.value
    elif str_val == 'devunittest':
        env_val = PU.DBNames.DevUnitTest.value
    elif str_val == 'produnittest':
        env_val = PU.DBNames.ProdUnitTest.value
    elif str_val == 'postgres':
        env_val = PU.DBNames.Default.value
    else:
        raise argparse.ArgumentTypeError(f'Invalid database environment: {str_val}')
            
    return env_val

# --- Post-parse cross-argument validation ---
def _cross_arg_validate_args(args):
    if args.num_cancellations > args.num_bookings:
        parser.error('-nca (--num-cancellations) must be less than or equal to -nbo (--num-bookings)')

# --- Post-parse validation ---
def _post_parse_validate_args(args):
    generator_args = ['-nbu', '--num-buildings', '-nro', '--num-rooms', '-nus', '--num-users', '-nbo', '--num-bookings', '-nca', '--num-cancellations']
    user_set_generator_args = any(arg in sys.argv for arg in generator_args)

    if user_set_generator_args and not args.generate:
        print('WARNING: Generator parameters have been specified but generator mode (-g / --generate) was not enabled. These parameters will be ignored.', file=sys.stderr)

    _cross_arg_validate_args(args)

# --- Argument parsing ---
def parse_args():
    parser = argparse.ArgumentParser(
        prog='DataPopulator', 
        description='DataPopulator populates the database :D',
        epilog='¯\\_(ツ)_/¯')
    
    parser.add_argument('-e', '--environment', type=_database_env, default='postgres', help='database environment: toy, dev, prod, toyunittest, devunittest, produnittest, or postgres')
    parser.add_argument('-d', '--directory', type=_dir_path, default='./Data', help='path of data directory (local storage of web scraped data and dataset subdirectories)')
    parser.add_argument('-r', '--random-seed', type=_positive_int, help='seed for randomizer')
    parser.add_argument('-o', '--overwrite', action='store_true', help='overwrite local generator resource (and web scraped files)')

    arg_group_scraper = parser.add_argument_group('web scraper options')
    arg_group_scraper.add_argument('-s', '--scrape', action='store_true', help='enable web scraping mode')

    arg_group_generator = parser.add_argument_group('data generator options')
    arg_group_generator.add_argument('-g', '--generate', action='store_true', help='enable data generator mode')
    arg_group_generator.add_argument('-nbu', '--num-buildings', type=_positive_int, default=1000, help='number of buildings to generate')
    arg_group_generator.add_argument('-nro', '--num-rooms', type=_positive_int, default=5000, help='number of rooms to generate')
    arg_group_generator.add_argument('-nus', '--num-users', type=_positive_int, default=1500, help='number of users to generate')
    arg_group_generator.add_argument('-nbo', '--num-bookings', type=_positive_int, default=100000, help='number of bookings to generate')
    arg_group_generator.add_argument('-nca', '--num-cancellations', type=_non_negative_int, default=2000, help='number of cancellations to generate')

    arg_group_populator = parser.add_argument_group('database populator options')
    arg_group_populator.add_argument('-p', '--populate', action='store_true', help='enable database population mode')

    args = parser.parse_args()
    _post_parse_validate_args(args)
    return args

# --- Here be dragons ---
def summarize_args(args):
    print('DataPopulator\n')
    print('Execution plan:')
    print(f"{'environment: ':<20}{args.environment}")
    print(f"{'directory: ':<20}{args.directory}")
    print(f"{'overwrite: ':<20}{args.overwrite}")
    print(f"{'scrape: ':<20}{args.scrape}")
    print(f"{'generate: ':<20}{args.generate}")
    print(f"{'  buildings: ':<20}{args.num_buildings}")
    print(f"{'  rooms: ':<20}{args.num_rooms}")
    print(f"{'  users: ':<20}{args.num_users}")
    print(f"{'  bookings: ':<20}{args.num_bookings}")
    print(f"{'  cancellations: ':<20}{args.num_cancellations}")
    print(f"{'populate: ':<20}{args.populate}")
    
def confirm_or_exit(prompt="Continue? [y/N]: "):
    try:
        response = input(prompt).strip().lower()
        if response not in ('y', 'yes'):
            print('Aborted')
            sys.exit(1)
    except KeyboardInterrupt:
        print('Aborted')
        sys.exit(1)
    print()