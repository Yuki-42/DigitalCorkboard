"""
Contains the Post class, which is used to represent a post in the database.
"""

# Standard library imports
from datetime import datetime

class Post:
    """
    Represents a post in the database.
    """

    # Type hinting
    ID: int
    CreatorId: int
    Title: str
    Content: str
    AddedOn: datetime
    ExpiresOn: datetime | None

    def __init__(self, post: tuple[int, int, str, str, datetime, datetime | None]):
        """
        Initializes a new instance of the Post class.

        Args:
            post (tuple[int, int, str, str, datetime, datetime]): The post tuple from the database.
        """

        self.ID = post[0]
        self.CreatorId = post[1]
        self.Title = post[2]
        self.Content = post[3]
        self.AddedOn = post[4]
        self.ExpiresOn = post[5]
