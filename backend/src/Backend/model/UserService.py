import uuid
import os
import FixRaidenBoss2 as FRB
from datetime import datetime, timezone
from typing import Optional, Tuple, Callable

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
            print(errorMsg)
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
            print("Permission level", permLevel)
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
