import os

import PyUtils as PU
import Backend as BK

from .BaseUnitTest import BaseUnitTest


class R8Test(BaseUnitTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.testFolder = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R8", "tests")
        cls.bookingService = BK.BookingService(cls.dbTool)

    def setUp(self):
        self.bookingId = None

    def tearDown(self):
        if (self.bookingId is not None):
            self.removeCancellation(self.bookingId)

    def removeCancellation(self, bookingId: str):
        sql = 'DELETE FROM "Cancellation" WHERE "bookingID" = %(bookingID)s;'
        self.dbTool.executeSQL(sql, vars = {"bookingID": bookingId}, commit = True)

    def runCancelTest(self, testName: str):
        args, kwargs = self.loadArgs(testName)

        success, msg = self.bookingService.cancelBooking(*args, **kwargs)
        self.bookingId = args[0]

        self.evalOutFile(msg, testName)

    # ======================================================

    def test_validCancellation_bookingCancelled(self):
        self.runCancelTest("cancelSuccess")

    def test_bookingNotExists_cancelFailed(self):
        self.runCancelTest("BookingNotExists")

    def test_userNotExists_cancelFailed(self):
        self.runCancelTest("UserNotExists")