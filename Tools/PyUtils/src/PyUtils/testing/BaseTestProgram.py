from typing import Dict, Any, Optional, Generic, List
import unittest, sys, argparse

from ..constants.GenericTypes import GenericTypes
from ..commands.BaseCommandBuilder import BaseCommandBuilder


# BaseTestProgram: Class used as the framework for running tests
class BaseTestProgram(unittest.TestProgram, Generic[GenericTypes.ConfigKey.value]):
    def __init__(self, description: str, cmdBuilderArgs: Optional[List[Any]] = None, cmdBuilderKwargs: Optional[Dict[str, Any]] = None, 
                 cmdBuilderCls = BaseCommandBuilder, epilog: str = "", *args, **kwargs):

        self._cmdBuilderCls = cmdBuilderCls
        self._cmdBuilderKwargs = cmdBuilderKwargs if (cmdBuilderKwargs is not None) else {}
        self._cmdBuilderArgs = cmdBuilderArgs if (cmdBuilderArgs is not None) else []

        self.description = description
        self.epilog = epilog
        self.testCommandBuilder: Optional[BaseCommandBuilder] = None

        self._isInit = True
        super().__init__(*args, **kwargs)
        self._isInit = False

    def _initArgParsers(self):
        self._main_parser = self._getParentArgParser()
        self.testCommandBuilder = self._cmdBuilderCls(*self._cmdBuilderArgs, argParser = self._main_parser, **self._cmdBuilderKwargs)

        self._main_parser = self.testCommandBuilder.argParser
        self._main_parser = self._getMainArgParser(self._main_parser)
        self._main_parser.description = self.description
        self.testCommandBuilder._argParser = self._main_parser

        self.testCommandBuilder.addEpilog(self.epilog)
        self.testCommandBuilder._argParser.formatter_class = argparse.RawTextHelpFormatter

        self._discovery_parser = self._getParentArgParser()
        self._discovery_parser = self._getDiscoveryArgParser(self._discovery_parser)

    def parseArgs(self, argv):
        if (not self._isInit):
            super().parseArgs(argv)
        else:
            self._initArgParsers()

        self.testCommandBuilder.parse()

    def runTests(self):
        if (not self._isInit):
            super().runTests()

    def run(self):
        self.parseArgs(sys.argv)
        self.runTests()
