from datetime import datetime, timezone
from functools import lru_cache
from tzlocal import get_localzone
import pytz
from typing import Optional, List


# DateTimeTool: Utility class for datetime functions
class DateTimeTool():
    StrFormats = ['%Y-%m-%d %I:%M:%S %p',
                  '%Y-%m-%d %H:%M:%S',

                  # Seriously Excel, what is wrong with your datetime autoconversion?
                  #   I try to disable your datatype conversion and you convert my datetime to number seconds since epoch time instead
                  '%Y-%m-%d %H:%M',
                  
                  # Used by Javascript
                  '%Y-%m-%dT%H:%M']
    
    @classmethod
    def getLocalDateTime(cls, dateTime: datetime):
        tzinfo = get_localzone()
        return dateTime.replace(tzinfo = tzinfo)

    # strToDateTime(dateTimeStr, formats): Converts a string to a datetime
    @classmethod
    def strToDateTime(cls, dateTimeStr: str, formats: Optional[List[str]] = None, tzinfo: Optional[str] = None) -> datetime:
        if (formats is None):
            formats = cls.StrFormats

        for format in formats:
            result = None
            try:
                result = datetime.strptime(dateTimeStr, format)
            except ValueError as e:
                continue

            result = cls.getLocalDateTime(result)
            if (tzinfo is None):
                return result
            return result.astimezone(tz = tzinfo)

        raise ValueError(f"The following datetime string ({dateTimeStr}) cannot be converted using any of the following formats: {formats}")