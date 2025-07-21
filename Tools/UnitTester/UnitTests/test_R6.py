import os
from typing import Optional, Tuple, List, Dict, Any

import PyUtils as PU
import Backend as BK

from .BaseUnitTest import BaseUnitTest


class R6Test(BaseUnitTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testFolder = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R6", "tests")
        cls.roomService = BK.RoomService(cls.dbTool)

    def parseArgs(self, testName: str, testFolder: Optional[str] = None) -> Tuple[List[Any], Dict[str, Any]]:
        args, kwargs = self.loadArgs(testName, testFolder = testFolder)
        return (args, kwargs)

    def runTest(self, testName: str):
        args, kwargs = self.parseArgs(testName)

        availableRooms = self.roomService.fetchAvailableRooms(*args, **kwargs)

        availableRoomsStr = []
        for roomData in availableRooms:
            availableRoomsStr.append(f"{roomData}")

        availableRoomsStr = "\n".join(availableRoomsStr)
        self.evalOutFile(availableRoomsStr, testName)

    # ======================================================

    def test_allParametersSpecified_filteredRooms(self):
        self.runTest("Public")