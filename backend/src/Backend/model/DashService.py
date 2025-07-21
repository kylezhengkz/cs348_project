import os
import uuid
from typing import Optional, Tuple

import PyUtils as PU
from .BaseAPIService import BaseAPIService
from ..view.BaseView import BaseView

class DashService(BaseAPIService):
    def __init__(self, dbTool: PU.DBTool, view: Optional[BaseView] = None):
        super().__init__(dbTool, view = view)

        self._prefix = "[DASH]"
        self._errorPrefix = "[DASH SQL ERROR]"

    def print(self, *args, **kwargs):
        prefix = self._prefix
        super().print(*args, **kwargs, prefix = prefix)

    def printError(self, *args, **kwargs):
        prefix = self._errorPrefix
        super().print(*args, **kwargs, prefix = prefix)

    def getDashboardMetrics(self, user_id: Optional[str]) -> Tuple[bool, dict]:
        try:
            userUUID = uuid.UUID(user_id)
        except ValueError:
            return [False, "Invalid UUID format for user ID."]

        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "AF2/AF2.sql")

        if not os.path.exists(sqlPath):
            return [False, f"Dashboard SQL file not found at {sqlPath}"]

        try:
            query = PU.DBTool.readSQLFile(sqlPath)
            self.print(f"Running getDashboardMetrics for {user_id}")
            self.print(f"SQL Path: {sqlPath}")
        except Exception as e:
            return [False, f"Error reading SQL file: {e}"]

        try:
            connData, cursor, error = self._dbTool.executeSQL(query,
                                                              vars={"user_id": str(userUUID)},
                                                              commit=False, closeConn=False)

            result = cursor.fetchone()
            self.print(f"Query result: {result}")
            connData.putConn()

            if result:
                return [True, {
                    "avg_duration_mins": result[0],
                    "most_booked_hour": result[1]
                }]
            else:
                return [False, "No booking data found."]
        except Exception as e:
            self.printError(f"{e}")
            return [False, f"SQL execution error: {e}"]
    
