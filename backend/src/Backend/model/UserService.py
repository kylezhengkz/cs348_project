import os
import uuid
from typing import Tuple

import PyUtils as PU

from .BaseAPIService import BaseAPIService


class UserService(BaseAPIService):
    def _getSignupErrorMsg(self, errorMsg: str) -> str:
        if ("User_email_key" in errorMsg):
          return "Email already exists"
        elif ("User_username_key" in errorMsg):
          return "Username already exists"
  
    def signup(self, username, email, password):
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R10/R10a.sql")
        try:
            with open(sqlPath, 'r') as f:
                signupSQL = f.read()
        except FileNotFoundError:
            return {
              "signupStatus": False,
              "errorMessage": f"Signup SQL file not found at {sqlPath}"
            }
        
        connData, cursor, error = self._dbTool.executeSQL(signupSQL, 
                                                          vars = {
                                                                  "username": username,
                                                                  "email": email,
                                                                  "passwrd": password
                                                                  },
                                                          commit = True, closeConn = False,
                                                          raiseException = False)
        
        if (error is not None):
            errorMsg = self._getSignupErrorMsg(f"{error}")
            self.print(errorMsg)
            return {
              "signupStatus": False,
              "errorMessage": errorMsg
            }
        
        row = cursor.fetchone()
        connData.putConn()

        if row:
            userId = row[0]
            return {
              "signupStatus": True,
              "userId": userId
            }
        else:
            return {
              "signupStatus": False,
              "errorMessage": "Unable to create user"
            }
    
    
    def login(self, username, password):
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R10/R10b.sql")
        try:
            with open(sqlPath, 'r') as f:
                loginSQL = f.read()
        except FileNotFoundError:
            return {
              "loginStatus": False,
              "errorMessage": f"Login SQL file not found at {sqlPath}"
            }
        
        connData, cursor, error = self._dbTool.executeSQL(loginSQL, 
                                                          vars = {
                                                                  "username": username,
                                                                  "passwrd": password
                                                                  },
                                                          commit = True, closeConn = False,
                                                          raiseException = False)
        
        if (error is not None):
            return {
              "loginStatus": False,
              "errorMessage": "Invalid credentials"
            }
        
        row = cursor.fetchone()
        connData.putConn()

        if row:
            userId = row[0]
            permLevel = row[1]
            self.print(f"Permission level {permLevel}")
            return {
              "loginStatus": True,
              "userId": userId,
              "permLevel": permLevel
            }
        else:
            return {
              "loginStatus": False,
              "errorMessage": "Unable to login",
            }
        
    def updateUsername(self, userId: uuid.UUID, oldUserName: str, newUserName: str) -> Tuple[bool, str]:
        try:
            query = """
            UPDATE "User"
            SET "userID" = %(new_username)s
            WHERE "userID" = %(old_username)s;
            """

            self.print(f"Updating username from {oldUserName} to {newUserName}")

            _, _, error = self._dbTool.executeSQL(query,
                                                vars={"old_username": oldUserName, "new_username": newUserName},
                                                commit=True)

            if error:
                self.printError(error)
                return [False, str(error)]
            return [True, "Username updated successfully."]
        except Exception as e:
            self.printError(e)
            return [False, str(e)]

    def updatePassword(self, user_id: uuid.UUID, old_password: str, new_password: str) -> Tuple[bool, str]:
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
