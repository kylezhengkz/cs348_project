import os
import uuid
from typing import Tuple

import PyUtils as PU
import pandas as pd

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
            
    def viewAdminLog(self, userID):
        sqlFile = os.path.join(PU.Paths.SQLFeaturesFolder.value, "AF4/AdminLog.sql")
        sql = PU.DBTool.readSQLFile(sqlFile)
        
        params = {
            'userID': userID
        }
        
        sqlEngine = self._dbTool.getSQLEngine()
        result = pd.read_sql(sql, sqlEngine, params = params)

        return result.to_dict('records')
        
    def updateUsername(self, userId: uuid.UUID, newUsername: str) -> Tuple[bool, str]:
        sqlFile = os.path.join(PU.Paths.SQLFeaturesFolder.value, "AF5/AF5a.sql")
        sql = PU.DBTool.readSQLFile(sqlFile)

        vars = {
            "newUsername": newUsername,
            "userId": f"{userId}"
        }

        try:
            _, _, error = self._dbTool.executeSQL(sql, vars=vars, commit=True)
            return [True, "Username updated successfully."]
        except Exception as e:
            self.print(e)
            return [False, str(e)]

    def updatePassword(self, userId: uuid.UUID, newPassword: str) -> Tuple[bool, str]:
      sqlFile = os.path.join(PU.Paths.SQLFeaturesFolder.value, "AF5/AF5b.sql")
      sql = PU.DBTool.readSQLFile(sqlFile)

      vars = {
          "newPassword": newPassword,
          "userId": f"{userId}"
      }

      try:
          _, _, error = self._dbTool.executeSQL(sql, vars=vars, commit=True)
          return [True, "Password updated successfully."]
      except Exception as e:
          self.print(e)
          return [False, str(e)]


