import os
import pytz
from typing import Optional, Tuple, List, Dict, Any

import PyUtils as PU
import Backend as BK

from .BaseUnitTest import BaseUnitTest


class R7Test(BaseUnitTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testFolder = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R7", "tests")
        cls.bookingService = BK.BookingService(cls.dbTool)

    def setUp(self):
        self.bookingId = None

    def tearDown(self):
        if (self.bookingId is not None):
            self.removeBooking(self.bookingId)

    def parseArgs(self, testName: str, testFolder: Optional[str] = None) -> Tuple[List[Any], Dict[str, Any]]:
        args, kwargs = self.loadArgs(testName, testFolder = testFolder)
        args[2] = PU.DateTimeTool.strToDateTime(args[2], tzinfo = pytz.utc)
        args[3] = PU.DateTimeTool.strToDateTime(args[3], tzinfo = pytz.utc)

        return (args, kwargs)
    
    def removeBooking(self, bookingId: str):
        sql = 'DELETE FROM "Booking" WHERE "bookingID" = %(bookingID)s;'
        self.dbTool.executeSQL(sql, vars = {"bookingID": bookingId}, commit = True)

    def runBookingTest(self, testName: str, convertUser: bool = True, convertRoom: bool = True):
        args, kwargs = self.parseArgs(testName)

        success, msg, bookingId = self.bookingService.bookRoom(*args, **kwargs)
        self.bookingId = bookingId

        result = "Booking Successful!" if (success) else msg
        self.evalOutFile(result, testName)

    # ======================================================

    def test_bookingAvailable_bookSuccess(self):
        self.runBookingTest("BookSuccess")

    def test_overlapBookingTime_bookFailed(self):
        self.runBookingTest("OverlapTime")

    def test_roomNotExists_bookFailed(self):
        self.runBookingTest("RoomNotExists")

    def test_userNotExists_bookFailed(self):
        self.runBookingTest("UserNotExists")

    def test_invalidBookStartTime_bookFailed(self):
        self.runBookingTest("InvalidStartTime")

    def test_invalidBookEndTime_bookFailed(self):
        self.runBookingTest("InvalidEndTime")

    def test_invalidTimeRange_bookFailed(self):
        self.runBookingTest("InvalidTimeRange")

    def test_bookingPast_bookFailed(self):
        self.runBookingTest("BookingAlreadyPast")

    def test_roomOverCapacity_bookFailed(self):
        self.runBookingTest("OverCapacity")