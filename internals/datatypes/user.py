"""
Contains the User class, which is used to represent a user in the database.
"""

from datetime import datetime


class User:
    """
    Represents a user in the database.
    """

    # Type hinting
    ID: int
    FirstName: str
    LastName: str
    Email: str
    Password: str
    Admin: bool
    Bio: str | None
    AddedOn: datetime

    def __init__(self, user: tuple[int, str, str, str, str, bool, str | None, datetime]):
        """
        Initializes a new instance of the User class.

        Args:
            user (tuple[int, str, str, str, str, bool, str, datetime]): The user tuple from the database.
        """

        self.ID = user[0]
        self.FirstName = user[1]
        self.LastName = user[2]
        self.Email = user[3]
        self.Password = user[4]
        self.Admin = user[5]
        self.Bio = user[6]
        self.AddedOn = user[7]
