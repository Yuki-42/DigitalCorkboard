"""
Contains the database class for the project.
"""

# Standard library imports
from asyncio import Queue
from datetime import datetime
from logging import LoggerAdapter
from sqlite3 import Connection, Cursor, OperationalError, ProgrammingError, connect
from os import getcwd, mkdir, path
from pathlib import Path

# Internal imports
from .config import Config
from .logging import createLogger


class Database:
    """
    Responsible for interfacing with the database.
    """

    def __init__(self, config: Config, databasePath: str | Path) -> None:
        """
        Initialises the database class.

        Returns:
            None
        """
        self.config: Config = config
        self.logger: LoggerAdapter = createLogger("Database", self.config.LoggingLevel)
        self.connection: Connection = connect(databasePath)

        # Check that the tables exist
        self._checkTablesExist()

    def __del__(self) -> None:
        """
        Closes the database connection.

        Returns:
            None
        """
        self.connection.close()

    def _checkTablesExist(self) -> None:
        """
        Checks that the tables exist in the database, and creates them if they do not.

        Returns:
            None
        """

        # Check that the tables exist
        self.logger.debug("Checking that the tables exist in the database.")
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables: list[tuple[str]] = cursor.fetchall()
        cursor.close()

        # If the tables do not exist, create them
        if len(tables) == 0:
            self.logger.debug("Tables do not exist in the database. Creating them.")
            cursor = self.connection.cursor()
            cursor.close()
            self.connection.commit()