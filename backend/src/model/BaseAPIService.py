import sys

from ..constants.Paths import UtilsPath

sys.path.insert(1, UtilsPath)

from PyUtils import DBTool


class BaseAPIService():
    def __init__(self, dbTool: DBTool):
        self._dbTool = dbTool