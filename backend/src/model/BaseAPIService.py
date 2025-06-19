import PyUtils as PU


class BaseAPIService():
    def __init__(self, dbTool: PU.DBTool):
        self._dbTool = dbTool