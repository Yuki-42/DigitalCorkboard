"""
Contains the config class for the bot.
"""

# Standard library imports
from json import load, dump
from logging import LoggerAdapter
from pathlib import Path

# Internal imports
from .logging import createLogger


class Config:
    """
    Responsible for interfacing with the configuration file.
    """

    # Type hinting
    path: str
    logger: LoggerAdapter

    def __init__(self, path: str | Path):
        self.path = path
        self.logger = createLogger("Config", self.LoggingLevel)

    @property
    def Logging(self) -> dict:
        """
        Gets the logging configuration from the config file.

        Returns:
            The logging configuration.
        """

        return self._getValue("Logging")

    @property
    def LoggingLevel(self) -> str:
        """
        Gets the logging level from the config file.

        Returns:
            The logging level.
        """

        return self._getValue("Logging")["Level"]

    @property
    def Server(self) -> dict:
        """
        Gets the server configuration from the config file.

        Returns:
            The server configuration.
        """

        return self._getValue("Server")

    @property
    def ServerHost(self) -> str:
        """
        Gets the server host from the config file.

        Returns:
            The server host.
        """

        return self._getValue("Server")["Host"]

    @property
    def ServerPort(self) -> int:
        """
        Gets the server port from the config file.

        Returns:
            The server port.
        """

        return self._getValue("Server")["Port"]

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
