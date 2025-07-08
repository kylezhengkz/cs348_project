import uuid
import os
import FixRaidenBoss2 as FRB
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Callable
import pytz

import PyUtils as PU

from .BaseAPIService import BaseAPIService


class BookingService(BaseAPIService):
    ErrorSearchDFA = {}
    
    def _getErrorMsg(self, dfaID: str, errorMsg: str, errorNotFoundMsg: str, dfaBuildFunc: Callable[[], FRB.BaseAhoCorasickDFA]) -> str:
        searchDFA = self.ErrorSearchDFA.get(dfaID)

        if (searchDFA is None):
            self.ErrorSearchDFA[dfaID] = dfaBuildFunc()

        keyword, val = self.ErrorSearchDFA[dfaID].getMaximal(errorMsg, errorOnNotFound = False)
        if (keyword is None):
            return errorNotFoundMsg
        
        if (val is not None):
            return val
        
        newLineInd = errorMsg.find("\n")
        return errorMsg[:newLineInd]
    
    def _buildBookingErrorSearchDFA(self) -> FRB.BaseAhoCorasickDFA:
        data = {
            "bookingendwindow": "Booking end time must be earlier than 11:00 PM UTC",
            "bookingstartwindow": "Booking start time must be later than 7:00 AM UTC",
            "validbookingcommitdate": "Booking time range must be later than the current time",
            "validbookingrange": "Booking time range is invalid",
            "RoomOverCapacityError": None,
            "Booking_userID_fkey": "User does not exist",
            "Booking_roomID_fkey": "Room does not exist",
            "Booking time overlaps with your own booking": "You already have a booking at a similar time!",
            "Room is already booked": "Room not available at this time"
        }

        return FRB.AhoCorasickBuilder().build(data = data)

    def _getBookingErrorMsg(self, errorMsg: str) -> str:
        return self._getErrorMsg("booking", errorMsg, "Booking encountered an unknown error!", self._buildBookingErrorSearchDFA)

    
    # bookRoom(userId, roomId, startTime, endTime, participants): Creates a new booking
    def bookRoom(self, userId: Optional[str], roomId: Optional[str], startTime: datetime, 
                 endTime: datetime, participants: Optional[str]) -> Tuple[bool, str, Optional[str]]:
        try:
            userUUID = uuid.UUID(userId)
            roomUUID = uuid.UUID(roomId)
        except ValueError:
            return [False, "Invalid UUID format for user ID or room ID.", None]
        
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R7/R7.sql")
        try:
            with open(sqlPath, 'r') as f:
                bookingSQL = f.read()
        except FileNotFoundError:
            return [False, f"Booking SQL file not found at {sqlPath}", None]
        
        connData, cursor, error = self._dbTool.executeSQL(bookingSQL, 
                                                          vars = {"userID": str(userUUID),
                                                                  "roomID": str(roomUUID),
                                                                  "bookDateTime": datetime.now(pytz.timezone("US/Eastern")).replace(tzinfo=None).replace(tzinfo=timezone.utc),
                                                                  "startTime": startTime,
                                                                  "endTime": endTime,
                                                                  "participants": participants}, 
                                                          commit = True, closeConn = False,
                                                          raiseException = False)
        
        if (error is not None):
            errorMsg = self._getBookingErrorMsg(f"{error}")
            return [False, errorMsg, None]
        
        row = cursor.fetchone()
        connData.putConn()

        if row:
            bookingId = row[0]
            return [True, f"Booking successful! Booking ID: {bookingId}", bookingId]
        else:
            return [False, "Booking failed: room does not exist or is already booked.", None]
        
    def _buildCancelErrorSearchDFA(self) -> FRB.BaseAhoCorasickDFA:
        data = {
            "CancelEarlierThanBookingError": None
        }

        return FRB.AhoCorasickBuilder().build(data = data)
    
    def _getCancelErrorMsg(self, errorMsg: str) -> str:
        return self._getErrorMsg("cancel", errorMsg, "Cancellation encountered an unknown error!", self._buildCancelErrorSearchDFA)

    # cancelBooking(booking_id, user_id): Cancels a booking
    def cancelBooking(self, booking_id: Optional[str], user_id: Optional[str]) -> Tuple[bool, str]:
        try:
            bookingUUID = uuid.UUID(booking_id)
            userUUID = uuid.UUID(user_id)
        except ValueError:
            return [False, "Invalid UUID format for booking ID or user ID."]
        
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R8/R8i.sql")
        try:
            cancelSQL = PU.DBTool.readSQLFile(sqlPath)
        except FileNotFoundError:
            return [False, f"Cancel SQL file not found at {sqlPath}"]
        
        connData, cursor, error = self._dbTool.executeSQL(cancelSQL, 
                                                          vars = {"booking_id": str(bookingUUID), 
                                                                  "user_id": str(userUUID),
                                                                  "cancel_date": datetime.now(timezone.utc)}, 
                                                          commit = True, closeConn = False,
                                                          raiseException = False)
        
        if (error is not None):
            errorMsg = self._getCancelErrorMsg(f"{error}")
            return [False, errorMsg]

        cancelledResultLen = cursor.rowcount
        connData.putConn()

        if cancelledResultLen > 0:
            return [True, "Booking successfully cancelled."]
        else:
            return [False, "Booking already cancelled or not found."]
        

    def getFutureBookings(self, user_id: str) -> Tuple[bool, list]:
    
        try:
            userUUID = uuid.UUID(user_id)
        except ValueError as e:
            return [False, "Invalid UUID format for user ID."]
    
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R8/R8ii.sql")
        
    
        if not os.path.exists(sqlPath):
            return [False, f"SQL file not found at {sqlPath}"]
    
        try:
            query = PU.DBTool.readSQLFile(sqlPath)
        except Exception as e:
            return [False, f"Error reading SQL file: {e}"]
    
        try:
            utc_now = datetime.now(timezone.utc)
            fake_utc_est_now = utc_now - timedelta(hours=4)
            now = fake_utc_est_now
            connData, cursor, error = self._dbTool.executeSQL(query,
                                                              vars={"user_id": str(userUUID), "now": now},
                                                              commit=False, closeConn=False)
            result = cursor.fetchall()
            connData.putConn()
            return [True, result]
        except Exception as e:
            return [False, f"SQL execution error: {e}"]