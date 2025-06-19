import uuid
import os
from datetime import datetime, timezone
from typing import Optional, Tuple

import PyUtils as PU

from .BaseAPIService import BaseAPIService


class BookingService(BaseAPIService):

    # bookRoom(userId, roomId, startTime, endTime, participants): Creates a new booking
    def bookRoom(self, userId: Optional[str], roomId: Optional[str], startTime: datetime, 
                 endTime: datetime, participants: Optional[str]) -> Tuple[bool, str]:
        try:
            userUUID = uuid.UUID(userId)
            roomUUID = uuid.UUID(roomId)
        except ValueError:
            return [False, "Invalid UUID format for user ID or room ID."]
        
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R7/R7.sql")
        try:
            with open(sqlPath, 'r') as f:
                bookingSQL = f.read()
        except FileNotFoundError:
            return False, f"Booking SQL file not found at {sqlPath}"
        
        connData, cursor, error = self._dbTool.executeSQL(bookingSQL, 
                                                          vars = {"userID": str(userUUID),
                                                                  "roomID": str(roomUUID),
                                                                  "bookDateTime": datetime.now(timezone.utc),
                                                                  "startTime": startTime,
                                                                  "endTime": endTime,
                                                                  "participants": participants}, 
                                                          commit = True, closeConn = False)
        
        row = cursor.fetchone()
        connData.putConn()

        if row:
            return [True, f"Booking successful! Booking ID: {row[0]}"]
        else:
            return [False, "Booking failed: room does not exist or is already booked."]

    # cancelBooking(booking_id, user_id): Cancels a booking
    def cancelBooking(self, booking_id: Optional[str], user_id: Optional[str]) -> Tuple[bool, str]:
        try:
            bookingUUID = uuid.UUID(booking_id)
            userUUID = uuid.UUID(user_id)
        except ValueError:
            return [False, "Invalid UUID format for booking ID or user ID."]
        
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R8/R8.sql")
        try:
            cancelSQL = PU.DBTool.readSQLFile(sqlPath)
        except FileNotFoundError:
            return [False, f"Cancel SQL file not found at {sqlPath}"]
        
        connData, cursor, error = self._dbTool.executeSQL(cancelSQL, 
                                                          vars = {"booking_id": str(bookingUUID), 
                                                                  "user_id": str(userUUID),
                                                                  "cancel_date": datetime.now(timezone.utc)}, 
                                                          commit = True, closeConn = False)

        cancelledResultLen = cursor.rowcount
        connData.putConn()

        if cancelledResultLen > 0:
            return [True, "Booking successfully cancelled."]
        else:
            return [False, "Booking already cancelled or not found."]