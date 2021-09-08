# -*- encoding: utf-8 -*-

__author__       = "Debmalya Pramanik"

__status__       = "production"
__version__      = "1.0"
__docformat__    = "camelCasing"

__copyright__    = "Copyright (c) 2020 Debmalya Pramanik"
__affiliation__  = "Indian Institute of Technology (IIT), Dhanbad"


import pymysql
import pymssql
import sqlalchemy as sa

class DBConnection(object):
    """Class to Connect to all the Popular Database using Python"""

    def __init__( self, username : str, password : str, hostname : str = 'localhost', database : str = 'database', **kwargs):
        # default constructor

        self.username = username
        self.password = password
        self.hostname = hostname
        self.database = database

        # keyword arguments
        self._db   = self.db_name(kwargs.get("db_name", "mysql"))
        self._port = kwargs.get("port", self._default_ports(self._db))
        self._conf = self._default_connectors(self._db) # default sa engine


    def db_name(self, name : str) -> str:
        """Format DB-Name and Return - for Consistency"""

        return name.lower()


    def _default_ports(self, dbName : str) -> int:
        # defines default port for populat db engines

        return {
            "mysql" : 3306,
            "mssql" : 1433
        }.get(dbName)


    def _default_connectors(self, name : str) -> str:
        # defines the default connectors

        return {
            "mysql" : "mysql+pymysql",
            "mssql" : "mssql+pymssql"
        }.get(name)


    @property
    def connectionString(self) -> str:
        """General Connection String for any DB Connection"""

        return f"{self.username}:{self.password}@{self.hostname}:{self._port}/{self.database}"


    @property
    def engineDialect(self):
        # {connectors} + {connection string}
        # https://docs.sqlalchemy.org/en/14/core/engines.html
        
        return f"{self._conf}://{self.connectionString}"


    @property
    def engine(self):
        return sa.create_engine(self.engineDialect)


    def connect(self):
        connection = self.engine.connect()
        return connection
    

    def __repr__(self):
        # representation

        return f"Connecting to {self.connectionString}"
