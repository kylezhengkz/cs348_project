import os
from datetime import datetime, timezone
import pandas as pd
import pytz
from typing import Optional, Dict, Any, List

import PyUtils as PU

from .BaseAPIService import BaseAPIService


class BuildingService(BaseAPIService):
    def fetchBuildings(self, buildingName: Optional[str] = None, addressLine1: Optional[str] = None, addressLine2: Optional[str] = None, 
                            city: Optional[str] = None, province: Optional[str] = None, country: Optional[str] = None, postalCode: Optional[str] = None) -> List[Dict[str, Any]]:
        
        sqlFile = os.path.join(PU.Paths.SQLFeaturesFolder.value, "GetBuildings/GetBuildings.sql")
        sql = PU.DBTool.readSQLFile(sqlFile)
                
        params = {
            'buildingName': f'%{buildingName}%' if buildingName and buildingName.strip() != '' else None,
            'addressLine1': f'%{addressLine1}%' if addressLine1 and addressLine1.strip() != '' else None,
            'addressLine2': f'%{addressLine2}%' if addressLine2 and addressLine2.strip() != '' else None,
            'city': f'%{city}%' if city and city.strip() != '' else None,
            'province': f'%{province}%' if province and province.strip() != '' else None,
            'country': f'%{country}%' if country and country.strip() != '' else None,
            'postalCode': f'%{postalCode}%' if postalCode and postalCode.strip() != '' else None,
        }
            
        sqlEngine = self._dbTool.getSQLEngine()
        result = pd.read_sql(sql, sqlEngine, params = params)

        return result.to_dict('records')
