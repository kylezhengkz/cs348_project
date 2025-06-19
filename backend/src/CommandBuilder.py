import argparse

from .constants.EnvironmentModes import EnvironmentModes


class CommandFormatter(argparse.MetavarTypeHelpFormatter, argparse.RawTextHelpFormatter):
    pass


class CommandBuilder():
    def __init__(self):
        self._argParser = argparse.ArgumentParser(description='Backend server for the room booking app', formatter_class=CommandFormatter)
        self._addArguments()
        self._args = argparse.Namespace()

    def parse(self) -> argparse.Namespace:
        self._args = self._argParser.parse_args()
        self.parseArgs()
        return self._args

    def parseArgs(self):
        if (self._args.env is None):
            self._args.env = EnvironmentModes.Toy
        else:
            foundEnv = EnvironmentModes.find(self._args.env)
            if (foundEnv is None):
                raise KeyError(f"No environment available for the name ({self._args.env})")
            
            self._args.env = foundEnv

    def _addArguments(self):
        self._argParser.add_argument("-e", "--env", action='store', type=str, help="What environment mode we want to run the backend")
        self._argParser.add_argument("-d", "--debug", action='store_true', help="Whether to turn on debugging mode")