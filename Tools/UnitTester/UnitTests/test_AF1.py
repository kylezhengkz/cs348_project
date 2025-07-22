import os
import uuid
import pytz
from typing import Optional, Tuple, List, Dict, Any

import PyUtils as PU
import Backend as BK

from .BaseUnitTest import BaseUnitTest


class AF1Test(BaseUnitTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testFolder = os.path.join(PU.Paths.SQLFeaturesFolder.value, "AF1", "tests")
        cls.dashboardService = BK.DashboardService(cls.dbTool)

    def parseArgs(self, testName: str, testFolder: Optional[str] = None) -> Tuple[List[Any], Dict[str, Any]]:
        args, kwargs = self.loadArgs(testName, testFolder = testFolder)
        return (args, kwargs)

    def runTest(self, testName: str):
        args, kwargs = self.parseArgs(testName)

        args[0] = uuid.UUID(args[0])

        if (args[1] is not None):
            args[1] = PU.DateTimeTool.strToDateTime(args[1], tzinfo = pytz.utc)

        if (args[2] is not None):
            args[2] = PU.DateTimeTool.strToDateTime(args[2], tzinfo = pytz.utc)

        success, result = self.dashboardService.getBookingFrequency(*args, **kwargs)
        resultStr = result

        if (success):
            resultStr = []
            for roomData in result:
                resultStr.append(f"{roomData}")

            resultStr = "\n".join(resultStr)

        self.evalOutFile(resultStr, testName)

    # ======================================================

    def test_invalidQueryLimit_queryFailed(self):
        self.runTest("InvalidQueryLimit")

    def test_invalidTimeRange_queryFailed(self):
        self.runTest("InvalidTimeRange")

    def test_userNotExsits_emptyQuery(self):
        self.runTest("UserNotExists")

    def test_allTimeRoomsNotLimit_allUserRooms(self):
        self.runTest("AllRooms")

    def test_roomsWithinTimeRange_filterRooms(self):
        self.runTest("RoomsInTimeRange")

    def test_topBookedRoom_only1Room(self):
        self.runTest("TopBookedRoom")