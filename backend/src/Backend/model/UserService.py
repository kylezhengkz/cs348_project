import uuid
import os
import FixRaidenBoss2 as FRB
from datetime import datetime, timezone
from typing import Optional, Tuple, Callable

import PyUtils as PU

from .BaseAPIService import BaseAPIService


class UserService(BaseAPIService):    
    def _getBookingErrorMsg(self, errorMsg: str) -> str:
        return self._getErrorMsg("booking", errorMsg, "Signup encountered an unknown error!", self._buildBookingErrorSearchDFA)
  
    def signup(self, username, email, password):
        sqlPath = os.path.join(PU.Paths.SQLFeaturesFolder.value, "R10/R10a.sql")
        try:
            with open(sqlPath, 'r') as f:
                bookingSQL = f.read()
        except FileNotFoundError:
            return [False, f"Booking SQL file not found at {sqlPath}", None]
        
        connData, cursor, error = self._dbTool.executeSQL(bookingSQL, 
                                                          vars = {
                                                                  "userID": username,
                                                                  "email": email,
                                                                  "passwrd": password
                                                                  },
                                                          commit = True, closeConn = False,
                                                          raiseException = False)
        
        if (error is not None):
            errorMsg = f"{error}"
            return [False, errorMsg, None]
        
        row = cursor.fetchone()
        connData.putConn()

        if row:
            userId = row[0]
            return [True, f"Signup successful! User ID: {userId}", userId]
        else:
            return [False, "Signup failed", None]
