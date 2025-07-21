from typing import Optional

import PyUtils as PU

from ..view.BaseView import BaseView


class BaseAPIService():
    def __init__(self, dbTool: PU.DBTool, view: Optional[BaseView] = None):
        self._view = view
        self._dbTool = dbTool

    def print(self, *args, **kwargs):
        if (self._view is None):
            return
        
        self._view.print(*args, **kwargs)