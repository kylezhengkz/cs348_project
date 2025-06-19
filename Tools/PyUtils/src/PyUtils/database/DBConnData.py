from psycopg2.extensions import connection
from psycopg2.pool import AbstractConnectionPool, PoolError
from typing import Optional


# DBConnData: Class for holding information about a database connection
class DBConnData():
    def __init__(self, conn: Optional[connection] = None, pool: Optional[AbstractConnectionPool] = None):
        self._conn = conn
        self._pool = pool

        self.checkConns()

    @property
    def conn(self) -> connection:
        return self._conn

    @conn.setter
    def conn(self, otherConn: connection):
        if (self._conn is not None):
            self.putConn()

        self._conn = otherConn
        self.checkConns()

    @property
    def pool(self) -> AbstractConnectionPool:
        return self._pool
    
    @pool.setter
    def pool(self, otherPool: AbstractConnectionPool):
        if (self._conn is not None):
            self.putConn()

        if (self._pool is not None):
            self._pool.closeall()

        self._pool = otherPool
        self.checkConns()

    def checkConns(self):
        if (self.conn is None and self.pool is None):
            raise KeyError("Cannot have connection being None and the pool being None")
    
    # getConn(): Retrieves a connection
    def getConn(self) -> connection:
        if (self._conn is None):
            self._conn = self._pool.getconn()

        return self._conn

    # putConn(): Closes or puts back a connection
    def putConn(self):
        if (self._pool is None):
            self._conn.close()
            return
        elif (self._conn is None):
            return

        try:
            self._pool.putconn(self._conn)
        except PoolError as e:
            self._conn.close()

        self._conn = None