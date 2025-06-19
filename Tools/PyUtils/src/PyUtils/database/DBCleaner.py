from psycopg2.sql import SQL, Identifier
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import Optional

from .DBTool import DBTool
from .DBConnData import DBConnData
from ..constants.TableNames import TableNames
from ..constants.DBFuncNames import DBFuncNames
from ..exceptions.AreYouSureError import AreYouSureError


# DBCleaner: Class to clean up tables and databases
class DBCleaner():
    def __init__(self, dbTool: DBTool):
        self._dbTool = dbTool

    # clearTable(tableName, isSure): Clears all the data from a table
    def clearTable(self, tableName: str, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"CLEAR ALL THE DATA IN THE TABLE BY THE NAME: '{tableName}' FOR THE DATABASE, '{self.database}'")
        
        sql = SQL("TRUNCATE {table} CASCADE;").format(table = Identifier(tableName))
        self._dbTool.executeSQL(sql, commit = True)

    # clearAll(isSure): Clears all the data from all the imported tables
    def clearAll(self, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"CLEAR ALL THE DATA IN THE DATABASE BY THE NAME '{self.database}'")

        for table in TableNames:
            self.clearTable(table.value, isSure = True)

    # deleteTable(tableName, isSure): Deletes a table
    def deleteTable(self, tableName: str, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"DELETE THE TABLE BY THE NAME: '{tableName}' FOR THE DATABASE, '{self.database}'")
        
        sql = SQL("DROP TABLE IF EXISTS {table} CASCADE;").format(table = Identifier(tableName))
        self._dbTool.executeSQL(sql, commit = True)

    # deleteAllTables(isSure): Deletes all the tables
    def deleteAllTables(self, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"DELETE ALL THE TABLES IN THE DATABASE BY THE NAME '{self.database}'")
        
        for table in TableNames:
            self.deleteTable(table.value, isSure = True)

    # deleteFunc(funcName, isSure): Deletes a function in the database
    def deleteFunc(self, funcName: str, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"DELETE THE FUNCTION BY THE NAME: '{funcName}' FOR THE DATABASE, '{self.database}'")
        
        sql = SQL("DROP FUNCTION IF EXISTS {func}").format(func = Identifier(funcName))
        self._dbTool.executeSQL(sql, commit = True)

    # deleteAllFuncs(isSure): Deletes all the functions in the database
    def deleteAllFuncs(self, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"DELETE ALL FUNCTIONS FOR THE DATABASE, '{self.database}'")
        
        for dbFunc in DBFuncNames:
            self.deleteFunc(dbFunc.value, isSure = True)

    # deleteDB(database, isSure): Deletes a database
    def deleteDB(self, database: Optional[str] = None, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"DELETE THE DATABASE BY THE NAME '{self.database}'")
        
        if (database is None):
            database = self._dbTool.database
        
        sql = SQL("DROP DATABASE {dbName} WITH (FORCE);").format(dbName = Identifier(database))

        connData = DBConnData(conn = self._dbTool.connectDB(defaultDB = True))
        connData.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Needed for creating/deleting databases

        self._dbTool.executeSQL(sql, connData = connData)
