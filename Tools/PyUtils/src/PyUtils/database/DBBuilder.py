import psycopg2
from psycopg2.sql import SQL, Identifier
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from typing import Union, Optional, List, Any, Dict, Tuple

from ..constants.TableNames import TableNames
from ..constants.DBFuncNames import DBFuncNames
from ..constants.Paths import Paths
from .DBTool import DBTool
from .DBConnData import DBConnData


# DBBuilder: Class to build tables and databases
class DBBuilder():
    NameIdentifiers = {"UserTable": Identifier(TableNames.User.value),
                       "BuildingTable": Identifier(TableNames.Buiding.value),
                       "RoomTable": Identifier(TableNames.Room.value),
                       "BookingTable": Identifier(TableNames.Booking.value),
                       "CancellationTable": Identifier(TableNames.Cancellation.value),
                        
                       "BookingParticipantsCheckFunc": Identifier(DBFuncNames.CheckBookingParticipants.value),
                       "CancellationDateTimeCheckFunc": Identifier(DBFuncNames.CheckCancellationDateTime.value)}

    def __init__(self, dbTool: DBTool):
        self._dbTool = dbTool
    
    # _setExtensions(): Sets the required extensions in the database
    def _setExtensions(self):
        sql = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'
        self._dbTool.executeSQL(sql, commit = True)

    # _grantOwnership(table, closeConn, connData): Grants ownership to the table
    def _grantOwnership(self, table: str, closeConn: bool = True, connData: Optional[DBConnData] = None):
        sql = SQL(f"ALTER TABLE IF EXISTS {{table}} OWNER to {{dbuser}}").format(table = Identifier(table), 
                                                                                 dbuser = Identifier(self._dbTool._secrets.username))
        self._dbTool.executeSQL(sql, vars = vars, commit = True, connData = connData, closeConn = closeConn)

    # _buildTable(table, sql, vars, closeConn, connData): Builds some generic table
    def _buildTable(self, table: str, sql: Union[str, SQL], vars: Optional[Union[List[Any], Dict[str, Any]]] = None, connData: Optional[DBConnData] = None, 
                    closeConn: bool = True, installExtensions: bool = True) -> Tuple[DBConnData, Optional[psycopg2.extensions.cursor]]:

        if (installExtensions):
            self._setExtensions()

        connData, cursor, error = self._dbTool.executeSQL(sql, vars = vars, closeConn = False, commit = True, connData = connData)
        self._grantOwnership(table, closeConn = closeConn, connData = connData)

        return (connData, cursor)

    # _buildTableFromFile(table, identifiers, vars, closeConn, connData, installExtensions): Builds some generic table based on some file
    def _buildTableFromFile(self, table: str, file: str, identifiers: Optional[Dict[str, Identifier]] = None, 
                            vars: Optional[Union[List[Any], Dict[str, Any]]] = None, closeConn: bool = True, 
                            connData: Optional[DBConnData] = None, installExtensions: bool = True) -> Tuple[DBConnData, Optional[psycopg2.extensions.cursor]]:
        
        if (identifiers is None):
            identifiers = {}

        sql = self._dbTool.readSQLFile(file)
        sql = SQL(sql).format(**identifiers)
        return self._buildTable(table, sql, vars = vars, closeConn = closeConn, connData = connData, installExtensions = installExtensions)

    # _buildTrigger(sql, vars, closeConn, connData): Builds a trigger
    def _buildTrigger(self, sql: Union[str, SQL], vars: Optional[Union[List[Any], Dict[str, Any]]] = None, closeConn: bool = True, 
                      connData: Optional[DBConnData] = None) -> Tuple[DBConnData, Optional[psycopg2.extensions.cursor]]:

        connData, cursor, error = self._dbTool.executeSQL(sql, vars = vars, closeConn = closeConn, commit = True, connData = connData)
        return connData, cursor

    # _buildTriggerFromFile(file, vars, closeConn, connData): Builds a trigger based on some file
    def _buildTriggerFromFile(self, file: str, identifiers: Optional[Dict[str, Identifier]] = None, 
                              vars: Optional[Union[List[Any], Dict[str, Any]]] = None, closeConn: bool = True, 
                              connData: Optional[DBConnData] = None) -> Tuple[DBConnData, Optional[psycopg2.extensions.cursor]]:

        if (identifiers is None):
            identifiers = {}

        sql = self._dbTool.readSQLFile(file)
        sql = SQL(sql).format(**identifiers)
        return self._buildTrigger(sql, vars = vars, closeConn = closeConn, connData = connData)

    # ============================================================


    # buildUserTable(): Builds the table for the Users
    def buildUserTable(self, installExtensions: bool = True):
        sqlFile = os.path.join(Paths.SQLTableCreationFolder.value, "CreateUser.sql")
        self._buildTableFromFile(TableNames.User.value, sqlFile, identifiers = self.NameIdentifiers, installExtensions = installExtensions)

    # buildBuildingTable(): Builds the table for the Buildings
    def buildBuildingTable(self, installExtensions: bool = True):
        sqlFile = os.path.join(Paths.SQLTableCreationFolder.value, "CreateBuilding.sql")
        self._buildTableFromFile(TableNames.Buiding.value, sqlFile, identifiers = self.NameIdentifiers, installExtensions = installExtensions)

    # buildRoomTable(): Builds the table for the rooms
    def buildRoomTable(self, installExtensions: bool = True):
        sqlFile = os.path.join(Paths.SQLTableCreationFolder.value, "CreateRoom.sql")
        self._buildTableFromFile(TableNames.Room.value, sqlFile, identifiers = self.NameIdentifiers, installExtensions = installExtensions)

    # buildBookingTable(): Builds the table for the bookings
    def buildBookingTable(self, installExtensions: bool = True):
        sqlFile = os.path.join(Paths.SQLTableCreationFolder.value, "CreateBooking.sql")
        connData, cursor = self._buildTableFromFile(TableNames.Room.value, sqlFile, identifiers = self.NameIdentifiers, installExtensions = installExtensions, closeConn = False)

        checkParticipantTriggerFile = os.path.join(Paths.SQLTriggerCreationFolder.value, "validBooking.sql")
        self._buildTriggerFromFile(checkParticipantTriggerFile, identifiers = self.NameIdentifiers, connData = connData)

    # buildCancellationTable(): Builds the table for the cancellations
    def buildCancellationTable(self, installExtensions: bool = True):
        sqlFile = os.path.join(Paths.SQLTableCreationFolder.value, "CreateCancellation.sql")
        connData, cursor = self._buildTableFromFile(TableNames.Room.value, sqlFile, identifiers = self.NameIdentifiers, installExtensions = installExtensions, closeConn = False)

        checkCancelDateTriggerFile = os.path.join(Paths.SQLTriggerCreationFolder.value, "validCancellation.sql")
        self._buildTriggerFromFile(checkCancelDateTriggerFile, identifiers = self.NameIdentifiers, connData = connData)

    # buildTables(): Builds all the necessary tables
    def buildTables(self):
        self.buildUserTable()
        self.buildBuildingTable(installExtensions = False)
        self.buildRoomTable(installExtensions = False)
        self.buildBookingTable(installExtensions = False)
        self.buildCancellationTable(installExtensions = False)

    # buildDB(database): Creates a database
    def buildDB(self, database: Optional[str] = None):
        if (database is None):
            database = self._dbTool.database

        sqlFile = os.path.join(Paths.SQLDBCreationFolder.value, "CreateDatabase.sql")
        identifiers = {"DatabaseName": Identifier(database), "OwnerName": Identifier(self._dbTool._secrets.username)}

        sql = self._dbTool.readSQLFile(sqlFile)
        sql = SQL(sql).format(**identifiers)

        connData = DBConnData(conn = self._dbTool.connectDB(defaultDB = True))
        connData.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Needed for creating/deleting databases

        self._dbTool.executeSQL(sql, vars = vars, connData = connData)

    # build(createDatabase): Build the all the required database and tabless
    def build(self, createDB: bool = False):
        if (createDB):
            self.buildDB()

        self.buildTables()