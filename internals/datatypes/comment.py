"""
Contains the Comment class which is used to represent a comment in the database.
"""

# Standard library imports
from datetime import datetime


class Comment:
    """
    Represents a comment in the database.
    """

    # Type hinting
    ID: int
    PostId: int
    CreatorId: int
    Content: str
    AddedOn: datetime
    EditedOn: datetime | None

    def __init__(self, comment: tuple[int, int, int, str, datetime, datetime | None]):
        """
        Initializes a new instance of the Comment class.

        Args:
            comment (tuple[int, int, int, str, datetime]): The comment tuple from the database.
        """

        self.ID = comment[0]
        self.PostId = comment[1]
        self.CreatorId = comment[2]
        self.Content = comment[3]
        self.AddedOn = comment[4]
        self.EditedOn = comment[5]
