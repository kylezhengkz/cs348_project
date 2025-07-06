import argparse

import PyUtils as PU

from .constants.EnvironmentModes import EnvironmentModes


class CommandBuilder(PU.BaseCommandBuilder):
    def __init__(self):
        argParser = argparse.ArgumentParser(description='Backend server for the room booking app', formatter_class=PU.CommandFormatter)
        super().__init__(argParser = argParser)

    def parseArgs(self) -> argparse.Namespace:
        super().parseArgs()

        if (self._args.env is None):
            self._args.env = EnvironmentModes.Toy
        else:
            foundEnv = EnvironmentModes.find(self._args.env)
            if (foundEnv is None):
                raise KeyError(f"No environment available for the name ({self._args.env})")
            
            self._args.env = foundEnv

        return self._args

    def _addArguments(self):
        self._argParser.add_argument("-e", "--env", action='store', type=str, help="What environment mode we want to run the backend")
        self._argParser.add_argument("-d", "--debug", action='store_true', help="Whether to turn on debugging mode")