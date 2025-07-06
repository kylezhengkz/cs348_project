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

    def run(self, suite: Optional[unittest.TestSuite] = None):
        self.parseArgs(sys.argv)
        self.runTests(suite = suite)