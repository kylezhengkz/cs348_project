import unittest
import os
import json
from pathlib import Path
from unittest import mock
from typing import Dict, TypeVar, Optional, Tuple, List, Any

import PyUtils as PU
import UnitTester as UT


T = TypeVar("T")

class PatchService:
    def _cleanup(self, patch, target):
        patch.stop()
        self.patches.pop(target)

    def patch(self, target, *args, **kwargs):
        p = mock.patch(target, *args, **kwargs)
        patchedMock = p.start()
        self.addCleanup(self._cleanup, *[p, target])
        self.patches[target] = patchedMock

    def patchObj(self, target, *args, **kwargs):
        p = mock.patch.object(target, *args, **kwargs)
        patchedMock = p.start()
        self.addCleanup(self._cleanup, *[p, target])
        self.patches[target] = patchedMock


class BaseUnitTest(unittest.TestCase, PatchService):
    FileSuffixes = {
        UT.EnvironmentModes.Toy: "-toy",
        UT.EnvironmentModes.Dev: "-sample",
        UT.EnvironmentModes.Prod: "-production"
    }

    @classmethod
    def setUpClass(cls):
        cls.patches: Dict[str, mock.Mock] = {}
        cls.testFolder = ""
        cls.dbTool = UT.Config[UT.ConfigKeys.DbTool]

    # getTestFile(testName, fileExt, testFolder): Retrieves the 
    def getTestFile(self, testName: str, fileExt: str, testFolder: str) -> str:
        envMode = UT.Config[UT.ConfigKeys.EnvironmentMode]
        fileSuffix = self.FileSuffixes[envMode]

        return os.path.join(testFolder, testName, f"test{fileSuffix}{fileExt}")

    # createTestFolder(testName, testFolder): Create the folder to contain a particular test
    def createTestFolder(self, testName: str, testFolder: Optional[str] = None):
        if (testFolder is None):
            testFolder = self.testFolder

        folder = os.path.join(testFolder, testName)
        if (not os.path.isdir(folder)):
            Path(folder).mkdir(parents=True, exist_ok=True)
    
    # loadInputs(testName, testFolder, command): Loads the input data into the database
    def loadArgs(self, testName: str, testFolder: Optional[str] = None) -> Tuple[List[Any], Dict[str, Any]]:
        if (testFolder is None):
            testFolder = self.testFolder

        inputFile = self.getTestFile(testName, PU.FileExts.Args.value, testFolder)
        if (not os.path.isfile(inputFile)):
            return ([], {})

        result = {}
        with open(inputFile, 'r', encoding = PU.FileEncodings.UTF8.value) as file:
            result = json.load(file)

        return (result["args"], result["kwargs"])

    # writeOutput(result, outputFile): Writes the output to the .out file
    def writeOutput(self, result: str, outputFile: str):
        with open(outputFile, "w", encoding = PU.FileEncodings.UTF8.value) as f:
            f.write(result)

    # checkOutFileExists(outputFile): Checks if the output file exists
    def checkOutFileExists(self, outputFile: str):
        if (not os.path.isfile(outputFile)):
            raise FileNotFoundError(f"Test output File not found at: {outputFile}")   

    # compareOutFile(result, outputFile): Compares the result to the expected output in the
    #  .out file
    def compareOutFile(self, result: str, outputFile: str):
        self.checkOutFileExists(outputFile)
        
        expected = ""
        with open(outputFile, "r", encoding = PU.FileEncodings.UTF8.value) as f:
            expected = f.read()
        
        self.assertEqual(result, expected)

    # printOutFile(testName, outputFile): Prints the output from the .out file
    def printOutFile(self, testName: str, outputFile: str):
        self.checkOutFileExists(outputFile)

        expected = ""
        with open(outputFile, "r", encoding = PU.FileEncodings.UTF8.value) as f:
            expected = f.read()

        result = (
            "=======================================\n"
            "\n"
            f"Test Name: {testName}\n"
            "\n"
            f"--- Result ---\n"
            f"{expected}\n"
            f"--------------\n"
            "\n"
            "======================================="
        )

        print(result)

    # evalOutFile(result, testName, testFolder, command): Evaluates an output file
    def evalOutFile(self, result: str, testName: str, testFolder: Optional[str] = None, command: Optional[UT.Commands] = None):
        if (command is None):
            command = UT.Config[UT.ConfigKeys.Command]
        
        if (testFolder is None):
            testFolder = self.testFolder

        outputFile = self.getTestFile(testName, PU.FileExts.Out.value, testFolder)

        if (command == UT.Commands.ProduceOutputs):
            self.writeOutput(result, outputFile)

        elif (command == UT.Commands.RunSuite):
            self.compareOutFile(result, outputFile)

        elif (command == UT.Commands.PrintOutputs):
            self.printOutFile(testName, outputFile)