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
                bookingSQL = f.read()
        except FileNotFoundError:
            return [False, f"Booking SQL file not found at {sqlPath}", None]
        
        connData, cursor, error = self._dbTool.executeSQL(bookingSQL, 
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
            return [False, errorMsg, None]
        
        row = cursor.fetchone()
        connData.putConn()

        if row:
            userId = row[0]
            return [True, f"Signup successful! User ID: {userId}", userId]
        else:
            return [False, "Unable to create user", None]
    
    
    def login(self, username, password):
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R10/R10b.sql")
        try:
            with open(sqlPath, 'r') as f:
                bookingSQL = f.read()
        except FileNotFoundError:
            return [False, f"Booking SQL file not found at {sqlPath}", None]
        
        connData, cursor, error = self._dbTool.executeSQL(bookingSQL, 
                                                          vars = {
                                                                  "username": username,
                                                                  "passwrd": password
                                                                  },
                                                          commit = True, closeConn = False,
                                                          raiseException = False)
        
        if (error is not None):
            return [False, "Invalid credentials", None]
        
        row = cursor.fetchone()
        connData.putConn()

        if row:
            userId = row[0]
            return [True, f"Login successful! User ID: {userId}", userId]
        else:
            return [False, "Unable to login", None]
