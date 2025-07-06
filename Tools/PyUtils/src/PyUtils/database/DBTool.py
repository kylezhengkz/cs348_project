import psycopg2
import psycopg2.sql
from psycopg2.extras import execute_values
from psycopg2.pool import AbstractConnectionPool, SimpleConnectionPool
from psycopg2.extensions import connection
import sqlalchemy
import pandas as pd
from functools import lru_cache
import numpy as np

from typing import Union, Optional, List, Any, Dict, Tuple, Type

from ..constants.DBNames import DBNames
from ..constants.FileEncodings import FileEncodings
from .DBSecrets import DBSecrets
from .DBConnData import DBConnData


# DBTools: Class for some useful database operations
class DBTool():
    def __init__(self, secrets: DBSecrets, database: str = DBNames.Toy.value, useConnPool: bool = False):
        self._secrets = secrets
        self._database = database
        self._sqlEngine: Optional[sqlalchemy.engine.Engine] = None
        self._useConnPool = useConnPool
        self.connPools = {DBNames.Default.value: self.createConnPool(defaultDB = True)}

        if (useConnPool):
            self.connPools[self.database] = self.createConnPool()

    @property
    def database(self) -> str:
        return self._database
    
    @database.setter
    def database(self, otherDatabase: str) -> str:
        connPool = self.connPools.get(self.database)
        if (connPool is not None):
            connPool.closeall()

        self._database = otherDatabase
        self.connPools[otherDatabase] = self.createConnPool()

    @property
    def useConnPool(self) -> bool:
        return self._useConnPools
    
    @useConnPool.setter
    def useConnPool(self, otherUseConnPool: bool):
        if (self._useConnPool and not otherUseConnPool):
            self.connPools.pop(self.database, None)
        elif (not self._useConnPool and otherUseConnPool):
            self.connPools[self.database] = self.createConnPool()

        self._useConnPool = otherUseConnPool

    # connectDB(defaultDB): Creates a connection to a database
    def connectDB(self, defaultDB: bool = False) -> connection:
        database = DBNames.Default.value if (defaultDB) else self.database

        return psycopg2.connect(database = database, user = self._secrets.username, password = self._secrets.password, 
                                host = self._secrets.host, port = self._secrets.port)
    
    # closeDBPools(): Close all the database connection pools
    def closeDBPools(self):
        for pool in self.connPools:
            self.connPools[pool].closeall()
    
    # getSQlEngine(flush): Retrievess the SQL engine for executing queries
    def getSQLEngine(self, flush: bool = False) -> sqlalchemy.engine.Engine:
        if (self._sqlEngine is None or flush):
            self._sqlEngine = sqlalchemy.create_engine(f"postgresql+psycopg2://{self._secrets.username}:{self._secrets.password}@{self._secrets.host}/{self.database}")

        return self._sqlEngine
    
    # createConnPool(minConn, maxConn): Creates a connection pool
    def createConnPool(self, minConn: int = 1, maxConn: int = 20, defaultDB: bool = False, connPoolCls: Type[AbstractConnectionPool] = SimpleConnectionPool) -> AbstractConnectionPool:
        database = DBNames.Default.value if (defaultDB) else self.database
        
        return connPoolCls(minConn, maxConn, user = self._secrets.username, password = self._secrets.password,
                           host = self._secrets.host, port = self._secrets.port, database = database)
    
    # getConn(defaultDB): Retrieves a connection from the preset connection pool in this object
    def getConn(self, defaultDB: bool = False) -> DBConnData:
        database = DBNames.Default.value if (defaultDB) else self.database

        if (self._useConnPool):
            connPool = self.connPools[database]
            return DBConnData(conn = connPool.getconn(), pool = connPool)

        conn = self.connectDB(defaultDB = defaultDB)
        return DBConnData(conn = conn)
    
    # putConn(conn, defaultDB): Puts a connection into the connection pool
    def putConn(self, conn: connection, defaultDB: bool = False):
        database = DBNames.Default.value if (defaultDB) else self.database
        self.connPools[database].putconn(conn)
    
    # resetSQLRead(): Clears the cache of the saved SQL queries read from files
    @classmethod
    def resetSQLRead(cls):
        cls.readSQLFile.cache_clear()

    @classmethod
    def _readSQLFile(cls, file: str) -> str:
        sql = ""
        with open(file, mode = "r", encoding = FileEncodings.UTF8.value) as f:
            sql = f.read()

        return sql

    # readSQLCachedFile(file): Reads some file containing SQL with memoization
    @classmethod
    @lru_cache(maxsize = 128)
    def readSQLCachedFile(cls, file: str) -> str:
        return cls._readSQLFile(file)


    # readSQLFile(file, cached): Reads some file containing SQL
    @classmethod
    def readSQLFile(cls, file: str, cached: bool = True) -> str:
        if (cached):
            return cls.readSQLCachedFile(file)
        return cls._readSQLFile(file)
    
    # executeSQL(sql, vars, commit, closeConn): Execute some SQL query
    def executeSQL(self, sql: Union[str, psycopg2.sql.SQL], vars: Optional[Union[List[Any], Dict[str, Any]]] = None, commit: bool = False, 
                   closeConn: bool = True, connData: Optional[DBConnData] = None, 
                   raiseException: bool = True) -> Tuple[DBConnData, Optional[psycopg2.extensions.cursor], Optional[Exception]]:
        
        if (connData is None):
            connData = self.getConn()

        conn = connData.getConn()
        if (conn.closed != 0 and connData.pool is None):
            conn = self.connectDB()
            connData.conn = conn

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
                connData.putConn()

        if (error is not None and raiseException):
            raise error

        return (connData, cursor, error)
    
    # insert(data, tableName): Inserts data from a CSV file to a table
    def insert(self, data: Union[str, pd.DataFrame], tableName: str, returnCols: Optional[List[str]] = None) -> Optional[pd.DataFrame]:
        if (isinstance(data, str)):
            data = pd.read_csv(data)

        data = data.replace(np.nan, None)

        # let pandas handle how to insert a dataframe if we do not need return values
        if (returnCols is None or not returnCols):
            sqlEngine = self.getSQLEngine()
            data.to_sql(tableName, sqlEngine, if_exists = "append", index = False)
            return

        colPrefix = "col"
        returnPrefix = "ret"
        columnParams = ",".join(map(lambda col: "{" + f"{colPrefix}{col}" + "}", data.columns))
        returnParams = ",".join(map(lambda col: "{" + f"{returnPrefix}{col}" + "}", returnCols))
        
        identifiers = {"table": psycopg2.sql.Identifier(tableName)}
        for col in data.columns:
            identifiers[f"{colPrefix}{col}"] = psycopg2.sql.Identifier(col)

        for col in returnCols:
            identifiers[f"{returnPrefix}{col}"] = psycopg2.sql.Identifier(col)
        
        values = [tuple(x) for x in data.to_numpy()]

        sql = psycopg2.sql.SQL(f"INSERT INTO {{table}} ({columnParams}) VALUES %s RETURNING {returnParams}").format(**identifiers)

        returnVals = []
        connData = self.getConn()
        conn = connData.getConn()

        if (conn.closed != 0 and connData.pool is None):
            conn = self.connectDB()
            connData.conn = conn

        cursor = conn.cursor()

        # https://stackoverflow.com/questions/5439293/is-insert-returning-guaranteed-to-return-things-in-the-right-order
        #
        # I cross my fingers that what this dude says is true
        #   and return values are generally in the order tuples are inserted
        try:
            returnVals = execute_values(cursor, sql, values, fetch = True)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            connData.putConn()

        result = pd.DataFrame(returnVals, columns = returnCols)
        return result