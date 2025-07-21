import unittest
import sys
from typing import Optional

import PyUtils as PU

from .config import Config
from .commandBuilder import CommandBuilder


# UnitTestProgram: Framework for running the overall integration tests
class UnitTestProgram(PU.BaseTestProgram[PU.GenericTypes.ConfigKey.value]):
    def __init__(self, *args, **kwargs):
        description = "Unit Tester for the backend SQL queries"
        super().__init__(description, cmdBuilderArgs = [description, Config], 
                         cmdBuilderCls = CommandBuilder, *args, **kwargs)
        
    def runTests(self, suite: Optional[unittest.TestSuite] = None):
        if (suite is not None):
            self.test = suite

        if (not self._isInit):
            super().runTests()

    def _do_discovery(self, argv, Loader=None):
        self.start = PU.Paths.UnitTestsFolder.value
        self.pattern = 'test*.py'
        self.top = None
        if argv is not None:
            # handle command line args for test discovery
            if self._discovery_parser is None:
                # for testing
                self._initArgParsers()
            self._discovery_parser.parse_args(argv, self)

        self.createTests(from_discovery=True, Loader=Loader)

    def createTests(self, from_discovery=False, Loader=None):
        if self.testNamePatterns:
            self.testLoader.testNamePatterns = self.testNamePatterns
        if from_discovery:
            loader = self.testLoader if Loader is None else Loader()
            self.test = loader.discover(self.start, self.pattern, self.top)
            return

        import UnitTests as UT
        if self.testNames is None:
            self.test = self.testLoader.loadTestsFromModule(UT)
        else:
            self.test = self.testLoader.loadTestsFromNames(self.testNames, UT)

    def run(self, suite: Optional[unittest.TestSuite] = None):
        self.parseArgs(sys.argv)
        self.runTests(suite = suite)