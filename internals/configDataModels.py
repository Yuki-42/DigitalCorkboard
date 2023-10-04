"""
Contains the data models for the config file. Each data model is a class that represents a section of the config file.
"""


class Server:
    """
    Represents the server section of the config file.
    """

    # Type hinting
    Host: str
    Port: int
    SecretKey: str

    def __init__(self, server: dict[str, str | int]):
        """
        Initializes a new instance of the Server class.

        Args:
            server (dict[str, str | int]): The server section of the config file.
        """

        self.Host = server["Host"]
        self.Port = server["Port"]
        self.SecretKey = server["SecretKey"]


class Logging:
    """
    Represents the logging section of the config file.
    """

    # Type hinting
    Level: str

    def __init__(self, logging: dict[str, str]):
        """
        Initializes a new instance of the Logging class.

        Args:
            logging (dict[str, str]): The logging section of the config file.
        """

        self.Level = logging["Level"]
