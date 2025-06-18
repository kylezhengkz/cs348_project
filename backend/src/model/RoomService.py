import sys
from datetime import datetime
import pandas as pd
from typing import Optional, Dict, Any

from .BaseAPIService import BaseAPIService
from ..constants.Paths import UtilsPath

sys.path.insert(1, UtilsPath)

from PyUtils import DateTimeTool


class RoomService(BaseAPIService):
    
    # fetchAvailableRooms(roomName, minCapacity, maxCapacity, startTimeStr, endTimeStr): Retrieves all the available rooms
    def fetchAvailableRooms(self, roomName: Optional[str] = None, minCapacity:Optional[str] = None, maxCapacity: Optional[str] = None, 
                            startTimeStr: Optional[str] = None, endTimeStr: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        
        useCurrent = True
        current_datetime = datetime.now()

        if (startTimeStr is not None and endTimeStr is not None):
            useCurrent = False

            try:
                dtStartTime = DateTimeTool.strToDateTime(startTimeStr)
                dtEndTime = DateTimeTool.strToDateTime(endTimeStr)
            except ValueError:
                useCurrent = True

        query = ('SELECT "buildingName", "roomName", count(bo."bookEndDateTime") as bookings, "capacity", "addressLine1", "addressLine2", '
        '"city", "province", "country", "postalCode" ')
            
        query += (
        'FROM "Building" bu '
        'JOIN "Room" r ON bu."buildingID" = r."buildingID" '
        'LEFT OUTER JOIN "Booking" bo ON bo."roomID" = r."roomID" '
        'AND bo."bookingID" NOT IN (SELECT "bookingID" FROM "Cancellation") '
        )
        
        if useCurrent:
            query += (
            'AND (bo."bookStartDateTime" > \'{}\' '
            'OR bo."bookEndDateTime" < \'{}\') '
            .format(current_datetime, current_datetime)
            )
        else:
            query += (
            'AND (bo."bookEndDateTime" < \'{}\' '
            'OR bo."bookStartDateTime" > \'{}\') '
            .format(dtStartTime, dtEndTime)
            )
        
        params = {}
        
        query += 'WHERE TRUE '
        
        if roomName:
            query += 'AND "roomName" ILIKE %(roomName)s '
            params["roomName"] = f'%{roomName}%'
        
        if minCapacity:
            query += 'AND "capacity" >= %(minCapacity)s '
            params["minCapacity"] = f"{minCapacity}"
        
        if maxCapacity:
            query += 'AND "capacity" <= %(maxCapacity)s '
            params["maxCapacity"] = f"{maxCapacity}"
        
        query += (
        'GROUP BY '
        '"buildingName", "roomName", "capacity", "addressLine1", "addressLine2", '
        '"city", "province", "country", "postalCode" '
        )

        sqlEngine = self._dbTool.getSQLEngine()
        result = pd.read_sql(query, sqlEngine, params = params)
        return result.to_dict('records')