# -*- encoding: utf-8 -*-

"""
The Database Connection Module Object

An all purpose, multi-flavored supported database connection object
for `sqlalchemy` oriented `create_engine` dialect.

Copyright (c) 2024 nxlogics, neuralNOD INC
"""

import os
import yaml

from sqlalchemy import create_engine


class DBConnection(object):
    """
    A Config-Parametric Class Object to Connect to Multi-Flavor DBs

    This is a general purpose connection object, that can be used to
    connect to any type of database using `python` SQL connection
    libraries. Currently, the class is defined for MySQL and MSSQL
    Server, but given the simplicity of the code, all different types
    of database can be easily controlled.

    ! All the parameters are controlled using the configuration file
    that has to be configured as `config/database.conf`, or may allow
    custom configuration file of the same type. (TODO)

    .. refactoring: all the attributes are now available as keyword
    arguments, while the recommendation is to use the `.conf` file.
    Bypass the use of `.conf` file by setting `bypass_conf = True`,
    however, in that case all the attributes are must using keyword
    arguments.

    Keyword Arguments
    :param username: Username for connecting to the database.
    :param password: Authenticationpassword.
    :param hostname: Hostname IP address, defaults to `locahost`
    :param database: Name of the database.

    :param port: Port at which the database is accessible. By default
    it connects to 3306 port for MySQL server,
    and 1433 port for MSSQL server.
    :param db_name: Name of the database to connect to. Defaults to
    MySQL Server.

    Example(s): The following can be used to understand the connect
    and run query for any type of database:

    ```python
      obj = DBConnection(
        username = "root",
        password = "pass",
        database = "dummy"
      )
      con = obj.connect()

      result = con.execute("SELECT * FROM `table-name`")
      for row in result:
        print(row)

      con.close()
    ```

    Configure other keyword arguments to control any other parameters.
    """

    def __init__(
            self,
            instance : str,
            bypass_conf : bool = False,
            **kwargs
    ) -> None:
        """
        Default Constructor of the Class DBConnection

        The default constructor is defined to fetch the data from the
        config file, as defined under `./config` of the directory, or
        allows the use of keyword arguments (refactoring).

        :type  instance: str
        :param instance: Name of the instance, custom define one/many
            from the configuration file. The default `localhost` instance
            is provided in the `dabase.conf-proto` that highlights the
            structure and usage.

        :type  bypass_conf: bool
        :param bypass_conf: To bypass the configuration file, and use
            the old convention, set the parameter to True, this allows
            the use of the keyword arguments. However, if set to false,
            the keyword arguuments are ignored w/o and error.
        """

        self.instance = instance
        
        if bypass_conf:
            # directly assign a value via keyword arguments
            self.username = kwargs.get("username", None)
            self.password = kwargs.get("password", None)
            self.hostname = kwargs.get("hostname", None)
            self.database = kwargs.get("database", None)
        else:
            self.__read_config__(self.instance)

        # keyword arguments
        self._db   = self.db_name(kwargs.get("db_name", "mysql"))
        self._port = kwargs.get("port", self._default_ports(self._db))
        self._conf = self._default_connectors(self._db) # default sa engine


    def __read_config__(self, instance : str) -> dict:
        from globals import CONFIG

        fname = "database.yaml-proto"
        with open(os.path.join(CONFIG, fname), "r") as f:
            config = yaml.load(f, Loader = yaml.FullLoader)

        config_data = config["configurations"][instance] # redundancy use

        # get the flavors/variants of the database, and driver name
        self.flavor = config_data["flavor"]
        self.driver = config_data["driver"]

        global_path_vars = config_data["global_path_variables"]
        if global_path_vars:
            # ignore individual path settings, and define value
            host = config_data["host"]["value"]
            port = config_data["port"]["value"]

            username = config_data["username"]["value"]
            password = config_data["password"]["value"]
            database = config_data["database"]["value"]
        else:
            # check individual settings, and set value
            func = lambda check, value : os.getenv(value) if check else value

            host = func(*config_data["host"].values())
            port = func(*config_data["port"].values())

            username = func(*config_data["username"].values())
            password = func(*config_data["password"].values())
            database = func(*config_data["database"].values())

        self.host = host
        self.port = port

        self.username = username
        self.password = password
        self.database = database

        return config


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
        return create_engine(self.engineDialect)


    def connect(self):
        connection = self.engine.connect()
        return connection
    

    def __repr__(self):
        # representation

        return f"Connecting to {self.connectionString}"
