import unittest
import sys
import os
import signal
import traceback
import psycopg2
from typing import Optional, Type

import PyUtils as PU

from .config import Config
from .constants.ConfigKeys import ConfigKeys
from .constants.EnvironmentModes import EnvironmentModes
from .tools.TestFileTools import TestFileTools
from .unitTestProgram import UnitTestProgram


class UnitTester():
    DbTool = None
    Singleton = None

    DBNames = {
        EnvironmentModes.Toy: PU.DBNames.ToyUnitTest.value,
        EnvironmentModes.Dev: PU.DBNames.DevUnitTest.value,
        EnvironmentModes.Prod: PU.DBNames.ProdUnitTest.value
    }

    def __init__(self):
        envPath = os.path.join(PU.Paths.ProjectFolder.value, ".env")
        self._secrets = PU.DBSecrets.load() if (os.path.isfile(envPath)) else PU.DBSecrets()
        self._dbname = PU.DBNames.Default.value

        self.DbTool = PU.DBTool(self._secrets, database = self._dbname, useConnPool = False)
        self._dbBuilder = PU.DBBuilder(self.DbTool)
        self._dbCleaner = PU.DBCleaner(self.DbTool)

        self._testLoader = unittest.TestLoader()
        self._testSuite = unittest.TestSuite()

        Config[ConfigKeys.DbCleaner] = self._dbCleaner
        Config[ConfigKeys.DbTool] = self.DbTool

    @classmethod
    def create(cls):
        if (cls.Singleton is None):
            cls.Singleton = cls()

        return cls.Singleton

    def setup(self):
        self.registerShutdown()

    def addTestSuite(self, testCls: Type[unittest.TestCase]):
        test = self._testLoader.loadTestsFromTestCase(testCls)
        self._testSuite.addTest(test)

    def _updateDBSecrets(self):
        newSecrets = Config[ConfigKeys.UserDBSecrets]

        if (newSecrets.username != ""):
            self._secrets.username = newSecrets.username

        if (newSecrets.password != ""):
            self._secrets.password = newSecrets.password

        if (newSecrets.host != ""):
            self._secrets.host = newSecrets.host

        if (newSecrets.port != ""):
            self._secrets.port = newSecrets.port

    def _run(self):
        with open(TestFileTools.UnitTestResultsFile, "w", encoding = PU.FileEncodings.UTF8.value) as f:
            runner = unittest.TextTestRunner(f)
            unitTester = UnitTestProgram(testRunner=runner, exit = False)
            unitTester.testCommandBuilder.parse()

            self._updateDBSecrets()
            self.DbTool._secrets = self._secrets

            environmentMode = Config[ConfigKeys.EnvironmentMode]
            self._dbname = self.DBNames[environmentMode]
            self.DbTool.database = self._dbname
            self.DbTool.useConnPool = True

            unitTester.run(self._testSuite)

        testResults = TestFileTools.readTestResults()
        print(testResults)

        testScore = testResults.split("\n", 1)[0]
        if (testScore.find("F") > -1 or testScore.find("E") > -1):
            raise PU.TesterFailed("unit")

    def tearDown(self):
        try:
            self.DbTool.closeDBPools()
        except psycopg2.pool.PoolError:
            pass

    def shutdown(self, sig: Optional[int] = None, frame: Optional[int] = None):
        self.tearDown()
        sys.exit(0)

    def registerShutdown(self):
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def run(self):
        self.setup()

        try:
            self._run()
        except Exception as e:
            print(traceback.format_exc())
        finally:
            self.tearDown()