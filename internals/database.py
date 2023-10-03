"""
Contains the database class for the project.
"""

# Standard library imports
from asyncio import Queue
from datetime import datetime
from logging import LoggerAdapter
from random import SystemRandom
from sqlite3 import Connection, Cursor, OperationalError, ProgrammingError, connect
from os import getcwd, mkdir, path
from pathlib import Path
from hashlib import sha512

# External imports
from passlib import hash

# Internal imports
from .config import Config
from .logging import createLogger

"""
Cryptographic related code snippet for reference (from disbroad):
```
# Creates password hash
hashedPassword = hash.pbkdf2_sha512.hash(plaintextPassword)
self.logger.debug(f"Generated hashed password: {hashedPassword}")

apiKey: str = sha512(
            f"{time().hex()}{hashedPassword}{username}{email}".encode()).hexdigest()
            

# Verifies password hash            
return hash.pbkdf2_sha512.verify(password, storedPassword)

"""


class Database:
    """
    Responsible for interfacing with the database.
    """
    secureRandom: SystemRandom = SystemRandom()

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
        tables: list[str] = [tableName[0] for tableName in cursor.fetchall()]
        cursor.close()

        # If the tables do not exist, create them
        if len(tables) == 0:
            self.logger.debug("Tables do not exist in the database. Creating them.")
            cursor = self.connection.cursor()
            cursor.execute(
                """
            CREATE TABLE IF NOT EXISTS Users (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                FirstName TEXT NOT NULL,
                LastName TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL,
                Admin BOOL DEFAULT FALSE,
                Bio TEXT,
                AddedOn DATETIME NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS Posts (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                CreatorId INTEGER NOT NULL,
                Title TEXT NOT NULL,
                Content TEXT NOT NULL,
                AddedOn DATETIME NOT NULL,
                ExpiresOn DATETIME,
                FOREIGN KEY (CreatorId) REFERENCES Users(Id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS Tags (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Description TEXT,
                Colour TEXT NOT NULL,
                AddedOn DATETIME NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS Comments (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                PostId INTEGER NOT NULL,
                UserId INTEGER NOT NULL,
                Content TEXT NOT NULL,
                AddedOn DATETIME NOT NULL,
                EditedOn DATETIME,
                DeletedOn DATETIME,
                FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
                FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
            );
            
            CREATE TABLE IF NOT EXISTS PostTags (
                PostId INTEGER NOT NULL,
                TagId INTEGER NOT NULL,
                FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
                FOREIGN KEY (TagId) REFERENCES Tags(Id) ON DELETE CASCADE
            );""")
            cursor.close()
            self.connection.commit()

        if "Users" not in tables:
            self.logger.error("Users table does not exist in the database. Recreating it.")
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Users (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    FirstName TEXT NOT NULL,
                    LastName TEXT NOT NULL,
                    Email TEXT NOT NULL UNIQUE,
                    Password TEXT NOT NULL,
                    Admin BOOL DEFAULT FALSE,
                    Bio TEXT,
                    AddedOn DATETIME NOT NULL
                );""")
            cursor.close()
            self.connection.commit()

        if "Posts" not in tables:
            self.logger.error("Posts table does not exist in the database. Recreating it.")
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Posts (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    CreatorId INTEGER NOT NULL,
                    Title TEXT NOT NULL,
                    Content TEXT NOT NULL,
                    AddedOn DATETIME NOT NULL,
                    ExpiresOn DATETIME,
                    FOREIGN KEY (CreatorId) REFERENCES Users(Id) ON DELETE CASCADE
                );""")
            cursor.close()
            self.connection.commit()

        if "Tags" not in tables:
            self.logger.error("Tags table does not exist in the database. Recreating it.")
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Comments (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PostId INTEGER NOT NULL,
                    UserId INTEGER NOT NULL,
                    Content TEXT NOT NULL,
                    AddedOn DATETIME NOT NULL,
                    EditedOn DATETIME,
                    DeletedOn DATETIME,
                    FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
                    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
                );""")
            cursor.close()
            self.connection.commit()

        if "Comments" not in tables:
            self.logger.error("Comments table does not exist in the database. Recreating it.")
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Comments (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    PostId INTEGER NOT NULL,
                    UserId INTEGER NOT NULL,
                    Content TEXT NOT NULL,
                    AddedOn DATETIME NOT NULL,
                    EditedOn DATETIME,
                    DeletedOn DATETIME,
                    FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
                    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
                );""")
            cursor.close()
            self.connection.commit()

        if "PostTags" not in tables:
            self.logger.error("PostTags table does not exist in the database. Recreating it.")
            cursor = self.connection.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS PostTags (
                    PostId INTEGER NOT NULL,
                    TagId INTEGER NOT NULL,
                    FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
                    FOREIGN KEY (TagId) REFERENCES Tags(Id) ON DELETE CASCADE
                );""")
            cursor.close()
            self.connection.commit()

    """
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Add Methods
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    def addUser(self, firstName: str, lastName: str, email: str, password: str) -> int:
        """
        Adds a user to the database.

        Args:
            firstName (str): The first name of the user.
            lastName (str): The last name of the user.
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            The id of the user added.
        """
        self.logger.info(f"Adding user '{firstName} {lastName}'({email}) to the database.")

        # Hash the password
        hashedPassword: str = hash.pbkdf2_sha512.hash(password)

        # Add the user to the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Users (FirstName, LastName, Email, Password, AddedOn) VALUES (?, ?, ?, ?, ?);", [firstName, lastName, email, hashedPassword, datetime.now()])
        self.connection.commit()

        # Get the id of the user added
        cursor.execute("SELECT Id FROM Users WHERE Email = ?;", (email,))
        userId: int = cursor.fetchone()[0]
        cursor.close()

        return userId

    def addPost(self, creatorId: int, title: str, content: str, expiresOn: datetime) -> int:
        """
        Adds a post to the database.

        Args:
            creatorId (int): The id of the user who created the post.
            title (str): The title of the post.
            content (str): The content of the post.
            expiresOn (datetime): The datetime the post expires on.

        Returns:
            The id of the post added.
        """
        self.logger.info(f"Adding post '{title}' to the database.")

        # Add the post to the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Posts (CreatorId, Title, Content, AddedOn, ExpiresOn) VALUES (?, ?, ?, ?, ?);", [creatorId, title, content, datetime.now(), expiresOn])
        self.connection.commit()

        # Get the id of the post added
        cursor.execute("SELECT Id FROM Posts WHERE Title = ?;", [title])
        postId: int = cursor.fetchone()[0]
        cursor.close()

        return postId

    def addTag(self, name: str, description: str, colour: str) -> int:
        """
        Adds a tag to the database.

        Args:
            name (str): The name of the tag.
            description (str): The description of the tag.
            colour (str): The colour of the tag.

        Returns:
            The id of the tag added.
        """
        self.logger.info(f"Adding tag '{name}' to the database.")

        # Add the tag to the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Tags (Name, Description, Colour, AddedOn) VALUES (?, ?, ?, ?);", [name, description, colour, datetime.now()])
        self.connection.commit()

        # Get the id of the tag added
        cursor.execute("SELECT Id FROM Tags WHERE Name = ?;", [name])
        tagId: int = cursor.fetchone()[0]
        cursor.close()

        return tagId

    def addComment(self, postId: int, userId: int, content: str) -> int:
        """
        Adds a comment to the database.

        Args:
            postId (int): The id of the post the comment is on.
            userId (int): The id of the user who created the comment.
            content (str): The content of the comment.

        Returns:
            The id of the comment added.
        """
        self.logger.info(f"Adding comment '{content}' to the database.")

        # Add the comment to the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Comments (PostId, UserId, Content, AddedOn) VALUES (?, ?, ?, ?);", [postId, userId, content, datetime.now()])
        self.connection.commit()

        # Get the id of the comment added
        cursor.execute("SELECT Id FROM Comments WHERE Content = ?;", [content])
        commentId: int = cursor.fetchone()[0]
        cursor.close()

        return commentId

    def addPostTag(self, postId: int, tagId: int) -> None:
        """
        Adds a post tag to the database.

        Args:
            postId (int): The id of the post that the tag is on.
            tagId (int): The id of the tag the post tag is on.

        Returns:
            None
        """
        self.logger.info(f"Adding post tag '{postId} {tagId}' to the database.")

        # Add the post tag to the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("INSERT INTO PostTags (PostId, TagId) VALUES (?, ?);", [postId, tagId])
        self.connection.commit()
        cursor.close()
