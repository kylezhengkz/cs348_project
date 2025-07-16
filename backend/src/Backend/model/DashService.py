import os
import uuid
from typing import Optional, Tuple

import PyUtils as PU
from .BaseAPIService import BaseAPIService

class DashService(BaseAPIService):
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
            print("[DASH] Running getDashboardMetrics for", user_id)
            print("[DASH] SQL Path:", sqlPath)
        except Exception as e:
            return [False, f"Error reading SQL file: {e}"]

        try:
            connData, cursor, error = self._dbTool.executeSQL(query,
                                                              vars={"user_id": str(userUUID)},
                                                              commit=False, closeConn=False)

            result = cursor.fetchone()
            print("[DASH] Query result:", result)
            connData.putConn()

            if result:
                return [True, {
                    "avg_duration_mins": result[0],
                    "most_booked_hour": result[1]
                }]
            else:
                return [False, "No booking data found."]
        except Exception as e:
            print("[DASH SQL ERROR]", e)
            return [False, f"SQL execution error: {e}"]
    
