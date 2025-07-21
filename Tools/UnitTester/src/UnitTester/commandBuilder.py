import argparse
from typing import Dict, Any, Generic, Optional

import PyUtils as PU

from .constants.GenericTypes import GenericTypes
from .constants.Commands import Commands
from .constants.ConfigKeys import ConfigKeys
from .constants.CommandOpts import CommandOpts
from .constants.EnvironmentModes import EnvironmentModes
from .constants.ShortCommandOpts import ShortCommandOpts
from .exceptions.InvalidCommand import InvalidCommand


# CommandBuilder: Class for building the command for the unit tester
class CommandBuilder(PU.BaseCommandBuilder, Generic[GenericTypes.ConfigKey.value]):
    def __init__(self, description: str, configs: Dict[GenericTypes.ConfigKey.value, Any], 
                 argParser: Optional[argparse.ArgumentParser] = None, argParserKwargs: Optional[Dict[str, Any]] = None,
                 epilog: str = ""):

        if (argParserKwargs is None):
            argParserKwargs = {}

        super().__init__(argParser = argParser, argParserKwargs = {"description": description, "epilog": epilog, **argParserKwargs})
        self._configs = configs

    def _addArguments(self):
        allCommands = set(map(lambda command: f"  - {command}", Commands.getAll()))
        allCommands = "\n".join(allCommands)

        allEnvironments = set(map(lambda command: f"  - {command}", EnvironmentModes.getAll()))
        allEnvironments = "\n".join(allEnvironments)

        environmentOptHelpStr = f"The environment mode to run the tester.\nIf this option is not specified, then will run the tester against the datasets of every environment mode\n\nThe available environment modes are:\n{allEnvironments}"

        self._argParser.add_argument(ShortCommandOpts.EnvironmentMode.value, CommandOpts.EnvironmentMode.value, action='store', type=str, help=environmentOptHelpStr)
        self._argParser.add_argument(ShortCommandOpts.DBUserName.value, CommandOpts.DBUserName.value, action='store', type=str, help=f"Override the username to the database")
        self._argParser.add_argument(ShortCommandOpts.DBPassword.value, CommandOpts.DBPassword.value, action='store', type=str, help=f"Override the password to the database")
        self._argParser.add_argument(ShortCommandOpts.DBHost.value, CommandOpts.DBHost.value, action='store', type=str, help=f"Override the host to the database")
        self._argParser.add_argument(ShortCommandOpts.DBPort.value, CommandOpts.DBPort.value, action='store', type=str, help=f"Override the port to the database")
        
        self._argParser.add_argument("command", type=str, help=f"The command to run the unit tester.\n\nThe available commands are:\n{allCommands}")
        super()._addArguments()

    def _parseCommand(self):
        commandName = self._args.command
        command = Commands.match(commandName)

        if (command is None):
            raise InvalidCommand(commandName)
        else:
            self._configs[ConfigKeys.Command] = command

    def _parseEnvironment(self):
        environmentName = self._args.env
        if (environmentName is None):
            return

        environmentMode = EnvironmentModes.match(environmentName)
        if (environmentMode is None):
            raise KeyError(f"Environment mode by the name, '{environmentName}' is not found")
        else:
            self._configs[ConfigKeys.EnvironmentMode] = environmentMode

    def _parseDBSecrets(self):
        username = self._args.username
        password = self._args.password
        host = self._args.host
        port = self._args.port

        if (username is None):
            username = ""

        if (password is None):
            password = ""

        if (host is None):
            host = ""

        if (port is None):
            port = ""

        secrets = self._configs[ConfigKeys.UserDBSecrets]
        secrets.username = username
        secrets.password = password
        secrets.host = host
        secrets.port = port

    def parseArgs(self) -> argparse.Namespace:
        super().parseArgs()
        self._parseCommand()
        self._parseEnvironment()
        self._parseDBSecrets()
        return self._args
