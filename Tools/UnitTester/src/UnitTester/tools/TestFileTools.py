import os

import PyUtils as PU


# FileTools: Tools for file manipulation for the tester
class TestFileTools():
    UnitTestResultsFile = os.path.join(PU.Paths.UnitTesterFolder.value, 'UnitTestResults.txt')
    UnitTestOutputsFile = os.path.join(PU.Paths.UnitTesterFolder.value, 'UnitTestOutputs.txt')

    # readTestResults(): Reads the integration test results
    @classmethod
    def readTestResults(cls) -> str:
        result = ""
        with open(cls.UnitTestResultsFile, "r", encoding = PU.FileEncodings.UTF8.value) as f:
            result = f.read()
        return result

    # clearTestPrintOutputs(): Clears out the printing outputs
    @classmethod
    def clearTestPrintOutputs(cls):
        with open(cls.UnitTestOutputsFile, "w", encoding = PU.FileEncodings.UTF8.value) as f:
            f.write("")

    # addTestPrintOutputs(): Adds text into the printing outputs
    @classmethod
    def addTestPrintOutputs(cls, txt: str):
        with open(cls.UnitTestOutputsFile, "a", encoding = PU.FileEncodings.UTF8.value) as f:
            f.write(txt)