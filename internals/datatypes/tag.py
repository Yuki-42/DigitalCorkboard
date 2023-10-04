"""
Contains the Tag class which is used to represent a tag in the database.
"""

# Standard library imports
from datetime import datetime


class Tag:
    """
    Represents a tag in the database.
    """

    # Type hinting
    ID: int
    Name: str
    Description: str | None
    Colour: str
    AddedOn: datetime

    def __init__(self, tag: tuple[int, str, str | None, str, datetime]):
        """
        Initializes a new instance of the Tag class.

        Args:
            tag (tuple[int, str, str, str, datetime]): The tag tuple from the database.
        """

        self.ID = tag[0]
        self.Name = tag[1]
        self.Description = tag[2]
        self.Colour = tag[3]
        self.AddedOn = tag[4]
