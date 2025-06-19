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
        
        # Check if room exists
        sql = 'SELECT 1 FROM "Room" WHERE "roomID" = %s'
        connData, cursor, error = self._dbTool.executeSQL(sql, vars = (str(roomUUID),), closeConn = False)
        if not cursor.fetchone():
            return [False, "Room does not exist."]
        
        # Check for overlapping bookings
        sql = '''
              SELECT 1 FROM "Booking"
              WHERE "roomID" = %s
              AND NOT (%s >= "bookEndDateTime" OR %s <= "bookStartDateTime");
              '''
        connData, cursor, error = self._dbTool.executeSQL(sql, vars = (str(roomUUID), startTime, endTime), closeConn = False, connData = connData)
        if cursor.fetchone():
            return [False, "Room is already booked for the selected time."]
        
        # Inserting booking
        sqlFile = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R7/R7.sql")
        sql = PU.DBTool.readSQLFile(sqlFile)
        connData, cursor, error = self._dbTool.executeSQL(sql, vars = (str(userUUID), str(roomUUID), datetime.now(timezone.utc), startTime, endTime, participants), commit = True, connData = connData)
        booking_id = cursor.fetchone()[0]
        return [True, f"Booking successful! Booking ID: {booking_id}"]

    # cancelBooking(booking_id, user_id): Cancels a booking
    def cancelBooking(self, booking_id: Optional[str], user_id: Optional[str]) -> Tuple[bool, str]:
        try:
            bookingUUID = uuid.UUID(booking_id)
            userUUID = uuid.UUID(user_id)
        except ValueError:
            return [False, "Invalid UUID format for booking ID or user ID."]
        
        # Verify booking exists and belongs to the user
        sql = '''
                SELECT * FROM "Booking" 
                WHERE "bookingID" = %s AND "userID" = %s
            '''
        connData, cursor, error = self._dbTool.executeSQL(sql, vars = (str(bookingUUID), str(userUUID)), closeConn = False)
        booking = cursor.fetchone()
        if not booking:
            return [False, "Booking ID not found or does not belong to the user."]
        
        # check if the booking is already cancelled
        sql = 'SELECT "bookingID" FROM "Cancellation" WHERE "bookingID" = %s;'
        connData, cursor, error = self._dbTool.executeSQL(sql, vars = [str(bookingUUID)], closeConn = False)
        cancelledBooking = cursor.fetchone()
        if (cancelledBooking is not None):
            return [False, "The booking has already been cancelled."]
        
        # Insert into Cancellation table
        sqlFile = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R8/R8.sql")
        sql = PU.DBTool.readSQLFile(sqlFile)
        connData, cursor, error = self._dbTool.executeSQL(sql, vars = {"booking_id": str(bookingUUID), "user_id": str(userUUID)}, commit = True, connData = connData)

        return [True, "Booking successfully cancelled."]