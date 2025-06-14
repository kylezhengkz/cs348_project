import psycopg2
import psycopg2.sql
import sqlalchemy
import pandas as pd
from functools import lru_cache
import numpy as np

from typing import Union, Optional, List, Any, Dict, Tuple

from ..constants.DBNames import DBNames
from ..constants.FileEncodings import FileEncodings
from .DBSecrets import DBSecrets


# DBTools: Class for some useful database operations
class DBTool():
    def __init__(self, secrets: DBSecrets, database: str = DBNames.Toy.value):
        self._secrets = secrets
        self.database = database

    # connectDB(defaultDB): Creates a connection to a database
    def connectDB(self, defaultDB: bool = False) -> psycopg2.extensions.connection:
        database = DBNames.Default.value if (defaultDB) else self.database

        return psycopg2.connect(database = database, user = self._secrets.username, password = self._secrets.password, 
                                host = self._secrets.host, port = self._secrets.port)
    
    # createSQlEngine(): Creates the SQL engine for executing queries
    def createSQLEngine(self) -> sqlalchemy.engine.Engine:
        return sqlalchemy.create_engine(f"postgresql+psycopg2://{self._secrets.username}:{self._secrets.password}@{self._secrets.host}/{self.database}")
    
    # resetSQLRead(): Clears the cache of the saved SQL queries read from files
    @classmethod
    def resetSQLRead(cls):
        cls.readSQLFile.cache_clear()

    # readSQLFile(): Reads some file containing SQL with memoization
    @classmethod
    @lru_cache(maxsize = 128)
    def readSQLFile(cls, file: str) -> str:
        sql = ""
        with open(file, mode = "r", encoding = FileEncodings.UTF8.value) as f:
            sql = f.read()

        return sql
    
    # executeSQL(sql, vars, commit, closeConn): Execute some SQL query
    def executeSQL(self, sql: Union[str, psycopg2.sql.SQL], vars: Optional[Union[List[Any], Dict[str, Any]]] = None, commit: bool = False, 
                   closeConn: bool = True, conn: Optional[psycopg2.extensions.connection] = None, raiseException: bool = True) -> Tuple[psycopg2.extensions.connection, Optional[psycopg2.extensions.cursor], Optional[Exception]]:
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

        if (error is not None and raiseException):
            conn.close()
            raise error

        return (conn, cursor, error)
    
    # insert(data, tableName): Inserts data from a CSV file to a table
    def insert(self, data: Union[str, pd.DataFrame], tableName: str, returnCols: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
        if (isinstance(data, str)):
            data = pd.read_csv(data)

        data = data.replace(np.nan, None)

        # let pandas handle how to insert a dataframe if we do not need return values
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
            conn, cursor, err = self.executeSQL(sql, vars = tuple(row), commit = True, closeConn = False, conn = conn, raiseException = False)
            if (err is not None):
                break
            
            currentReturnVal = cursor.fetchone()
            returnVals.append(currentReturnVal)

        conn.close()
        if (err):
            raise err

        return pd.DataFrame(returnVals, columns = returnCols)