"""
Contains the config class for the bot.
"""

# Standard library imports
from json import load, dump
from logging import LoggerAdapter
from pathlib import Path

# Internal imports
from .logging import createLogger
from .configDataModels import Server, Logging


class Config:
    """
    Responsible for interfacing with the configuration file.
    """

    # Type hinting
    path: str
    logger: LoggerAdapter

    def __init__(self, path: str | Path):
        self.path = path
        self.logger = createLogger("Config", self.Logging.Level)

    @property
    def Logging(self) -> Logging:
        """
        Gets the logging configuration from the config file.

        Returns:
            The logging configuration.
        """

        return Logging(self._getValue("Logging"))

    @property
    def Server(self) -> Server:
        """
        Gets the server configuration from the config file.

        Returns:
            The server configuration.
        """

        return Server(self._getValue("Server"))

    def _getValue(self, key: str) -> any:
        """
        Gets the associated value of a key in the config file.

        Returns:
            The value of the key.

        Raises:
            KeyError: If the key does not exist.
        """

        with open(self.path, "r") as f:
            config: dict = load(f)

        if key not in config:
            raise KeyError(f"Key '{key}' does not exist in config file.")

        return config[key]

    def _setValue(self, key: str, value: any) -> None:
        """
        Sets the value of a key in the config file.

        Args:
            key: The key to set.
            value: The value to set.

        Returns:
            None
        """

        with open(self.path, "r") as f:
            config: dict = load(f)

        config[key] = value

        with open(self.path, "w") as f:
            dump(config, f, indent=4)
