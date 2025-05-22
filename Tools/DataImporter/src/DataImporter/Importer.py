import psycopg2
import pandas as pd
import os
import psycopg2.sql
import sqlalchemy
from typing import Optional, Union, List, Dict, Any, Tuple

from .DBSecrets import DBSecrets
from .AreYouSureError import AreYouSureError
from .ColNames import ColNames
from .TableNames import TableNames


# Importer: The importer for adding data into the database
class Importer():
    def __init__(self, secrets: DBSecrets):
        self.secrets = secrets

    # connectDB(): Creates a connection to the database
    def connectDB(self) -> psycopg2.extensions.connection:
        return psycopg2.connect(database = self.secrets.db, user = self.secrets.username, password = self.secrets.password, 
                                    host = self.secrets.host, port = self.secrets.port)
    
    def createSQLEngine(self) -> sqlalchemy.engine.Engine:
        return sqlalchemy.create_engine(f"postgresql+psycopg2://{self.secrets.username}:{self.secrets.password}@{self.secrets.host}/{self.secrets.db}")
    
    # executeSQL(sql, vars, commit, closeConn): Execute some SQL query
    def executeSQL(self, sql: Union[str, psycopg2.sql.SQL], vars: Optional[Union[List[Any], Dict[str, Any]]] = None, commit: bool = False, closeConn: bool = True, conn: Optional[psycopg2.extensions.connection] = None) -> Tuple[psycopg2.extensions.connection, Optional[psycopg2.extensions.cursor], Optional[Exception]]:
        if (conn is None):
            conn = self.connectDB()

        cursor = None
        error = None

        try:
            cursor = conn.cursor()
            cursor.execute(sql, vars = vars)

            if (commit):
                conn.commit()
        except Exception as e:
            error = e
            if (commit):
                conn.rollback()
        finally:
            if (closeConn):
                conn.close()

        return (conn, cursor, error)

    # insert(data, tableName): Inserts data from a CSV file to a table
    def insert(self, data: Union[str, pd.DataFrame], tableName: str, returnCols: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
        if (isinstance(data, str)):
            data = pd.read_csv(data)

        # let pandas handle how to insert a dataframe
        if (returnCols is None or not returnCols):
            sqlEngine = self.createSQLEngine()
            data.to_sql(tableName, sqlEngine, if_exists = "append", index = False)
            return

        colPrefix = "col"
        returnPrefix = "ret"
        insertParams = ", ".join(["%s"] * len(data.columns))
        columnParams = ",".join(map(lambda col: "{" + f"{colPrefix}{col}" + "}", data.columns))
        returnParams = ",".join(map(lambda col: "{" + f"{returnPrefix}{col}" + "}", returnCols))
        
        identifiers = {"table": psycopg2.sql.Identifier(tableName)}
        for col in data.columns:
            identifiers[f"{colPrefix}{col}"] = psycopg2.sql.Identifier(col)

        for col in returnCols:
            identifiers[f"{returnPrefix}{col}"] = psycopg2.sql.Identifier(col)

        sql = psycopg2.sql.SQL(f"INSERT INTO {{table}} ({columnParams}) VALUES ({insertParams}) RETURNING {returnParams}").format(**identifiers)
        returnVals = []
        err = None
        conn = self.connectDB()

        # insert each tuple individually to get the return values in the proper order
        for row in data.itertuples(index = False):
            conn, cursor, err = self.executeSQL(sql, vars = tuple(row), commit = True, closeConn = False, conn = conn)
            if (err is not None):
                break
            
            currentReturnVal = cursor.fetchone()
            returnVals.append(currentReturnVal)

        conn.close()
        if (err):
            raise err

        return pd.DataFrame(returnVals, columns = returnCols)

    # clearTable(tableName, isSure): Clears all the data from a table
    def clearTable(self, tableName: str, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"CLEAR ALL THE DATA IN THE TABLE BY THE NAME: {tableName}")
        
        sql = psycopg2.sql.SQL("TRUNCATE {table} CASCADE;").format(table = psycopg2.sql.Identifier(tableName))
        self.executeSQL(sql, commit = True)

    # clearAll(isSure): Clears all the data from all the imported tables
    def clearAll(self, isSure: bool = False):
        if (not isSure):
            raise AreYouSureError(f"CLEAR ALL THE DATA IN THE DATABASE")
        
        tablesToClear = [
            TableNames.User.value,
            TableNames.Buiding.value,
            TableNames.Room.value,
            TableNames.Booking.value
        ]

        for table in tablesToClear:
            print(f"Clearing {table}...")
            self.clearTable(table, isSure = True)

    # toDateTime(data, cols, format): Converts certain columns in the data to a datetime
    def toDateTime(self, data: pd.DataFrame, cols: List[str], format: Optional[str] = None) -> pd.DataFrame:
        if (format is None):
            format = '%Y-%m-%d %H:%M:%S'

        for col in cols:
            data[col] = pd.to_datetime(data[col], format = format)

        return data

    # replaceIds(data, originalIds, generatedIds, idColName): Replaces the ids in the original data with the newly generated ids
    def replaceIds(self, data: pd.DataFrame, originalIds: pd.DataFrame, generatedIds: pd.DataFrame, idColName: str) -> pd.DataFrame:
        tempIdColName = f"temp{idColName}"
        data = data.rename(columns = {idColName: tempIdColName})
        originalIds = originalIds.rename(columns = {idColName: tempIdColName})
        originalIds = pd.concat([originalIds, generatedIds], axis = 1)

        data = pd.merge(data, originalIds, on = tempIdColName, how = "left")
        data = data.drop(columns = [tempIdColName])
        return data
    
    # insertAndReplaceIds(dataToInsert, insertTableName, dataNeedingReplace, idColName): Inserts the data and replaces the foreign ids of the other
    #   tables with the newly generated ids after the data insertion
    def insertAndReplaceIds(self, dataToInsert: pd.DataFrame, insertTableName: str, dataNeedingReplace: List[pd.DataFrame], idColName: str) -> Optional[Union[List[pd.DataFrame], pd.DataFrame]]:
        originalIds = dataToInsert[[idColName]]
        dataToInsert = dataToInsert.drop(idColName, axis = 1)

        generatedIds = self.insert(dataToInsert, tableName = insertTableName, returnCols = [idColName])

        if (not dataNeedingReplace):
            return

        dataNeedingReplaceLen = len(dataNeedingReplace)
        for i in range(dataNeedingReplaceLen):
            dataNeedingReplace[i] = self.replaceIds(dataNeedingReplace[i], originalIds, generatedIds, idColName)

        if (dataNeedingReplaceLen == 1):
            return dataNeedingReplace[0]
        return dataNeedingReplace

    # importData(dataFolder): Inserts all the data from a particular dataset
    def importData(self, dataFolder: str):
        userFile = os.path.join(dataFolder, "User.csv")
        buildingFile = os.path.join(dataFolder, "Building.csv")
        roomFile = os.path.join(dataFolder, "Room.csv")
        bookingFile = os.path.join(dataFolder, "Booking.csv")

        userData = pd.read_csv(userFile)
        buildingData = pd.read_csv(buildingFile)
        roomData = pd.read_csv(roomFile)
        bookingData = pd.read_csv(bookingFile)

        bookingData = self.toDateTime(bookingData, [ColNames.BookingStartTime.value, ColNames.BookingEndTime.value])

        print(f"Inserting User Data...")
        bookingData = self.insertAndReplaceIds(userData, TableNames.User.value, [bookingData], ColNames.UserId.value)

        print(f"Inserting Building Data...")
        roomData = self.insertAndReplaceIds(buildingData, TableNames.Buiding.value, [roomData], ColNames.BuildingId.value)

        print(f"Inserting Room Data...")
        bookingData = self.insertAndReplaceIds(roomData, TableNames.Room.value, [bookingData], ColNames.RoomId.value)

        print(f"Inserting Booking Data...")
        bookingData = bookingData.drop(ColNames.BookingId.value, axis = 1)
        self.insert(bookingData, TableNames.Booking.value)
        