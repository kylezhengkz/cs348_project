import psycopg2
import psycopg2.sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from typing import Union, Optional, List, Any, Dict, Tuple

from ..constants.TableNames import TableNames
from ..constants.DBFuncNames import DBFuncNames
from ..constants.Paths import Paths
from .DBTool import DBTool


# DBBuilder: Class to build tables and databases
class DBBuilder():
    NameIdentifiers = {"UserTable": psycopg2.sql.Identifier(TableNames.User.value),
                       "BuildingTable": psycopg2.sql.Identifier(TableNames.Buiding.value),
                       "RoomTable": psycopg2.sql.Identifier(TableNames.Room.value),
                       "BookingTable": psycopg2.sql.Identifier(TableNames.Booking.value),
                       "CancellationTable": psycopg2.sql.Identifier(TableNames.Cancellation.value),
                        
                       "BookingParticipantsCheckFunc": psycopg2.sql.Identifier(DBFuncNames.CheckBookingParticipants.value),
                       "CancellationDateTimeCheckFunc": psycopg2.sql.Identifier(DBFuncNames.CheckCancellationDateTime.value)}

    def __init__(self, dbTool: DBTool):
        self._dbTool = dbTool
    
    # _setExtensions(): Sets the required extensions in the database
    def _setExtensions(self):
        sql = 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'
        self._dbTool.executeSQL(sql, commit = True)

    # _grantOwnership(table, closeConn, conn): Grants ownership to the table
    def _grantOwnership(self, table: str, closeConn: bool = True, conn: Optional[psycopg2.extensions.connection] = None):
        sql = psycopg2.sql.SQL(f"ALTER TABLE IF EXISTS {{table}} OWNER to {{dbuser}}").format(table = psycopg2.sql.Identifier(table), 
                                                                                              dbuser = psycopg2.sql.Identifier(self._dbTool._secrets.username))
        self._dbTool.executeSQL(sql, vars = vars, commit = True, conn = conn, closeConn = closeConn)

    # _buildTable(table, sql, vars, closeConn, conn, installExtensions): Builds some generic table
    def _buildTable(self, table: str, sql: Union[str, psycopg2.sql.SQL], vars: Optional[Union[List[Any], Dict[str, Any]]] = None, 
                    closeConn: bool = True, conn: Optional[psycopg2.extensions.connection] = None, installExtensions: bool = True) -> Tuple[psycopg2.extensions.connection, Optional[psycopg2.extensions.cursor]]:

        if (installExtensions):
            self._setExtensions()

        conn, cursor, error = self._dbTool.executeSQL(sql, vars = vars, closeConn = False, commit = True, conn = conn)
        self._grantOwnership(table, conn = conn, closeConn = closeConn)

        return (conn, cursor)

    # _buildTableFromFile(table, identifiers, vars, closeConn, conn, installExtensions): Builds some generic table based on some file
    def _buildTableFromFile(self, table: str, file: str, identifiers: Optional[Dict[str, psycopg2.sql.Identifier]] = None, 
                            vars: Optional[Union[List[Any], Dict[str, Any]]] = None, closeConn: bool = True, 
                            conn: Optional[psycopg2.extensions.connection] = None, installExtensions: bool = True) -> Tuple[psycopg2.extensions.connection, Optional[psycopg2.extensions.cursor]]:
        
        if (identifiers is None):
            identifiers = {}

        sql = self._dbTool.readSQLFile(file)
        sql = psycopg2.sql.SQL(sql).format(**identifiers)
        return self._buildTable(table, sql, vars = vars, closeConn = closeConn, conn = conn, installExtensions = installExtensions)

    # _buildTrigger(sql, vars, closeConn, conn): Builds a trigger
    def _buildTrigger(self, sql: Union[str, psycopg2.sql.SQL], 
                      vars: Optional[Union[List[Any], Dict[str, Any]]] = None, closeConn: bool = True, 
                      conn: Optional[psycopg2.extensions.connection] = None) -> Tuple[psycopg2.extensions.connection, Optional[psycopg2.extensions.cursor]]:

        conn, cursor, error = self._dbTool.executeSQL(sql, vars = vars, closeConn = closeConn, commit = True, conn = conn)
        return conn, cursor

    # _buildTriggerFromFile(file, vars, closeConn, conn): Builds a trigger based on some file
    def _buildTriggerFromFile(self, file: str, identifiers: Optional[Dict[str, psycopg2.sql.Identifier]] = None, 
                              vars: Optional[Union[List[Any], Dict[str, Any]]] = None, closeConn: bool = True, 
                              conn: Optional[psycopg2.extensions.connection] = None):

        if (identifiers is None):
            identifiers = {}

        sql = self._dbTool.readSQLFile(file)
        sql = psycopg2.sql.SQL(sql).format(**identifiers)
        return self._buildTrigger(sql, vars = vars, closeConn = closeConn, conn = conn)

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
        conn, cursor = self._buildTableFromFile(TableNames.Room.value, sqlFile, identifiers = self.NameIdentifiers, installExtensions = installExtensions, closeConn = False)

        checkParticipantTriggerFile = os.path.join(Paths.SQLTriggerCreationFolder.value, "validBooking.sql")
        self._buildTriggerFromFile(checkParticipantTriggerFile, identifiers = self.NameIdentifiers, conn = conn)

    # buildCancellationTable(): Builds the table for the cancellations
    def buildCancellationTable(self, installExtensions: bool = True):
        sqlFile = os.path.join(Paths.SQLTableCreationFolder.value, "CreateCancellation.sql")
        conn, cursor = self._buildTableFromFile(TableNames.Room.value, sqlFile, identifiers = self.NameIdentifiers, installExtensions = installExtensions, closeConn = False)

        checkCancelDateTriggerFile = os.path.join(Paths.SQLTriggerCreationFolder.value, "validCancellation.sql")
        self._buildTriggerFromFile(checkCancelDateTriggerFile, identifiers = self.NameIdentifiers, conn = conn)

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
        identifiers = {"DatabaseName": psycopg2.sql.Identifier(database), "OwnerName": psycopg2.sql.Identifier(self._dbTool._secrets.username)}

        sql = self._dbTool.readSQLFile(sqlFile)
        sql = psycopg2.sql.SQL(sql).format(**identifiers)

        conn = self._dbTool.connectDB(defaultDB = True)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) # Needed for creating/deleting databases

        self._dbTool.executeSQL(sql, vars = vars, conn = conn)

    # build(createDatabase): Build the all the required database and tabless
    def build(self, createDB: bool = False):
        if (createDB):
            self.buildDB()

        self.buildTables()