from datetime import datetime
from typing import Optional, List


# DateTimeTool: Utility class for datetime functions
class DateTimeTool():
    StrFormats = ['%Y-%m-%d %I:%M:%S %p',
                  '%Y-%m-%d %H:%M:%S',

                  # Seriously Excel, what is wrong with your datetime autoconversion?
                  #   I try to disable your datatype conversion and you convert my datetime to number seconds since epoch time instead
                  '%Y-%m-%d %H:%M']

    # strToDateTime(dateTimeStr, formats): Converts a string to a datetime
    @classmethod
    def strToDateTime(cls, dateTimeStr: str, formats: Optional[List[str]] = None) -> datetime:
        if (formats is None):
            formats = cls.StrFormats

        for format in formats:
            try:
                return datetime.strptime(dateTimeStr, format)
            except ValueError as e:
                continue

        raise ValueError(f"The following datetime string ({dateTimeStr}) cannot be converted using any of the following formats: {formats}")