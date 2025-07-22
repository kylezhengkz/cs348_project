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
    
    def updateUsername(self, old_username: str, new_username: str) -> Tuple[bool, str]:
        try:
            query = """
            UPDATE "User"
            SET "userID" = %(new_username)s
            WHERE "userID" = %(old_username)s;
            """

            self.print(f"Updating username from {old_username} to {new_username}")

            _, _, error = self._dbTool.executeSQL(query,
                                                vars={"old_username": old_username, "new_username": new_username},
                                                commit=True)

            if error:
                self.printError(error)
                return [False, str(error)]
            return [True, "Username updated successfully."]
        except Exception as e:
            self.printError(e)
            return [False, str(e)]

    def updatePassword(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        try:
            check_query = """
            SELECT COUNT(*) FROM "User"
            WHERE "userID" = %(user_id)s AND "password" = %(old_password)s;
            """

            connData, cursor, error = self._dbTool.executeSQL(check_query,
                                                            vars={"user_id": user_id, "old_password": old_password},
                                                            commit=False, closeConn=False)

            if error:
                connData.putConn()
                self.printError(error)
                return [False, "Password check failed."]

            result = cursor.fetchone()
            if not result or result[0] == 0:
                connData.putConn()
                return [False, "Old password incorrect."]


            update_query = """
            UPDATE "User"
            SET "password" = %(new_password)s
            WHERE "userID" = %(user_id)s;
            """

            _, _, update_error = self._dbTool.executeSQL(update_query,
                                                        vars={"user_id": user_id, "new_password": new_password},
                                                        commit=True)

            connData.putConn()

            if update_error:
                self.printError(update_error)
                return [False, "Password update failed."]
            return [True, "Password updated successfully."]
        except Exception as e:
            self.printError(e)
            return [False, str(e)]

    
