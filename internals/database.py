"""
Contains the database class for the project.
"""

# Standard library imports
from datetime import datetime
from logging import LoggerAdapter
from pathlib import Path
from random import SystemRandom
from sqlite3 import Connection, Cursor, connect

# External imports
from passlib import hash

# Internal imports
from .config import Config
from .datatypes.comment import Comment
from .datatypes.post import Post
from .datatypes.postTag import PostTag
from .datatypes.tag import Tag
from .datatypes.user import User
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
                UserId INTEGER NOT NULL,
                Title TEXT NOT NULL,
                Content TEXT NOT NULL,
                AddedOn DATETIME NOT NULL,
                ExpiresOn DATETIME,
                FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
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
                    UserId INTEGER NOT NULL,
                    Title TEXT NOT NULL,
                    Content TEXT NOT NULL,
                    AddedOn DATETIME NOT NULL,
                    ExpiresOn DATETIME,
                    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
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
        Properties
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    @property
    def users(self) -> list[User]:
        """
        Gets all the users in the database.

        Returns:
            A list of all the users in the database.
        """
        self.logger.debug("Getting all of the users in the database.")

        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users;")
        users: list[User] = [User(*user) for user in cursor.fetchall()]
        cursor.close()

        return users

    @property
    def posts(self) -> list[Post]:
        """
        Gets all the posts in the database.

        Returns:
            A list of all the posts in the database.
        """
        self.logger.debug("Getting all of the posts in the database.")

        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Posts;")
        posts: list[Post] = [Post(*post) for post in cursor.fetchall()]
        cursor.close()

        return posts

    @property
    def tags(self) -> list[Tag]:
        """
        Gets all the tags in the database.

        Returns:
            A list of all the tags in the database.
        """
        self.logger.debug("Getting all of the tags in the database.")

        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Tags;")
        tags: list[Tag] = [Tag(*tag) for tag in cursor.fetchall()]
        cursor.close()

        return tags

    @property
    def comments(self) -> list[Comment]:
        """
        Gets all the comments in the database.

        Returns:
            A list of all the comments in the database.
        """
        self.logger.debug("Getting all of the comments in the database.")

        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Comments;")
        comments: list[Comment] = [Comment(*comment) for comment in cursor.fetchall()]
        cursor.close()

        return comments

    @property
    def postTags(self) -> list[PostTag]:
        """
        Gets all the post tags in the database.

        Returns:
            A list of all the post tags in the database.
        """
        self.logger.debug("Getting all of the post tags in the database.")

        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM PostTags;")
        postTags: list[PostTag] = [PostTag(*postTag) for postTag in cursor.fetchall()]
        cursor.close()

        return postTags

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
        cursor.execute("INSERT INTO Users (FirstName, LastName, Email, Password, AddedOn) VALUES (?, ?, ?, ?, ?);",
                       [firstName, lastName, email, hashedPassword, datetime.now()])
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
        cursor.execute("INSERT INTO Posts (UserId, Title, Content, AddedOn, ExpiresOn) VALUES (?, ?, ?, ?, ?);",
                       [creatorId, title, content, datetime.now(), expiresOn])
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
        cursor.execute("INSERT INTO Tags (Name, Description, Colour, AddedOn) VALUES (?, ?, ?, ?);",
                       [name, description, colour, datetime.now()])
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
        cursor.execute("INSERT INTO Comments (PostId, UserId, Content, AddedOn) VALUES (?, ?, ?, ?);",
                       [postId, userId, content, datetime.now()])
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

    """
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Remove Methods
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    def removeUser(self, userId: int) -> None:
        """
        Removes a user from the database.

        Args:
            userId (int): The id of the user to remove.

        Returns:
            None
        """
        self.logger.info(f"Removing user '{userId}' from the database.")

        # Remove the user from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Users WHERE Id = ?;", [userId])
        self.connection.commit()
        cursor.close()

    def removePost(self, postId: int) -> None:
        """
        Removes a post from the database.

        Args:
            postId (int): The id of the post to remove.

        Returns:
            None
        """
        self.logger.info(f"Removing post '{postId}' from the database.")

        # Remove the post from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Posts WHERE Id = ?;", [postId])
        self.connection.commit()
        cursor.close()

    def removeTag(self, tagId: int) -> None:
        """
        Removes a tag from the database.

        Args:
            tagId (int): The id of the tag to remove.

        Returns:
            None
        """
        self.logger.info(f"Removing tag '{tagId}' from the database.")

        # Remove the tag from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Tags WHERE Id = ?;", [tagId])
        self.connection.commit()
        cursor.close()

    def removeComment(self, commentId: int) -> None:
        """
        Removes a comment from the database.

        Args:
            commentId (int): The id of the comment to remove.

        Returns:
            None
        """
        self.logger.info(f"Removing comment '{commentId}' from the database.")

        # Remove the comment from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Comments WHERE Id = ?;", [commentId])
        self.connection.commit()
        cursor.close()

    def removePostTag(self, postId: int, tagId: int) -> None:
        """
        Removes a post tag from the database.

        Args:
            postId (int): The id of the post that the tag is on.
            tagId (int): The id of the tag the post tag is on.

        Returns:
            None
        """
        self.logger.info(f"Removing post tag '{postId} {tagId}' from the database.")

        # Remove the post tag from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("DELETE FROM PostTags WHERE PostId = ? AND TagId = ?;", [postId, tagId])
        self.connection.commit()
        cursor.close()

    """
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Update Methods
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    def updateUser(self, userId: int, firstName: str = None, lastName: str = None, email: str = None,
                   password: str = None, admin: bool = None, bio: str = None) -> None:
        """
        Updates a user in the database.

        Args:
            userId (int): The id of the user to update.
            firstName (str): The first name of the user.
            lastName (str): The last name of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            admin (bool): Whether the user is an admin.
            bio (str): The bio of the user.

        Returns:
            None
        """
        self.logger.info(f"Updating user '{userId}' in the database.")

        # Get the user from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE Id = ?;", [userId])
        user: User = User(*cursor.fetchone())

        # Update the user in the database
        cursor.execute(
            "UPDATE Users SET FirstName = ?, LastName = ?, Email = ?, Password = ?, Admin = ?, Bio = ? WHERE Id = ?;",
            [firstName if firstName is not None else user.FirstName,
             lastName if lastName is not None else user.LastName,
             email if email is not None else user.Email,
             hash.pbkdf2_sha512.hash(password) if password is not None else user.Password,
             admin if admin is not None else user.Admin,
             bio if bio is not None else user.Bio,
             userId])
        self.connection.commit()
        cursor.close()

    def updatePost(self, postId: int, creatorId: int = None, title: str = None, content: str = None,
                   expiresOn: datetime = None, tags: list[int] = None) -> None:
        """
        Updates a post in the database.

        Args:
            postId: The id of the post to update.
            creatorId: The id of the user who created the post.
            title: The title of the post.
            content: The content of the post.
            expiresOn: The datetime the post expires on.
            tags: The tags of the post.

        Returns:
            None
        """

        self.logger.info(f"Updating post '{postId}' in the database.")

        # Get the post from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Posts WHERE Id = ?;", [postId])
        post: Post = Post(*cursor.fetchone())

        # Update the post in the database
        cursor.execute(
            "UPDATE Posts SET UserId = ?, Title = ?, Content = ?, ExpiresOn = ? WHERE Id = ?;",
            [creatorId if creatorId is not None else post.CreatorId,
             title if title is not None else post.Title,
             content if content is not None else post.Content,
             expiresOn if expiresOn is not None else post.ExpiresOn,
             postId])

        # Create new list of tags (wipe old tags)
        if tags is not None:
            cursor.execute("DELETE FROM PostTags WHERE PostId = ?;", [postId])
            for tag in tags:
                cursor.execute("INSERT INTO PostTags (PostId, TagId) VALUES (?, ?);", [postId, tag])

        self.connection.commit()
        cursor.close()

    def updateTag(self, tagId: int, name: str = None, description: str = None, colour: str = None) -> None:
        """
        Updates a tag in the database.

        Args:
            tagId: The id of the tag to update.
            name: The name of the tag.
            description: The description of the tag.
            colour: The colour of the tag.

        Returns:
            None
        """

        self.logger.info(f"Updating tag '{tagId}' in the database.")

        # Get the tag from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Tags WHERE Id = ?;", [tagId])
        tag: Tag = Tag(*cursor.fetchone())

        # Update the tag in the database
        cursor.execute(
            "UPDATE Tags SET Name = ?, Description = ?, Colour = ? WHERE Id = ?;",
            [name if name is not None else tag.Name,
             description if description is not None else tag.Description,
             colour if colour is not None else tag.Colour,
             tagId])
        self.connection.commit()
        cursor.close()

    def updateComment(self, commentId: int, postId: int = None, userId: int = None, content: str = None,
                      editedOn: datetime = None) -> None:
        """
        Updates a comment in the database.

        Args:
            commentId: The id of the comment to update.
            postId: The id of the post the comment is on.
            userId: The id of the user who created the comment.
            content: The content of the comment.
            editedOn: The datetime the comment was edited on.

        Returns:
            None
        """

        self.logger.info(f"Updating comment '{commentId}' in the database.")

        # Get the comment from the database
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Comments WHERE Id = ?;", [commentId])
        comment: Comment = Comment(*cursor.fetchone())

        # Update the comment in the database
        cursor.execute(
            "UPDATE Comments SET PostId = ?, UserId = ?, Content = ?, AddedOn = ?, EditedOn = ? WHERE Id = ?;",
            [postId if postId is not None else comment.PostId,
             userId if userId is not None else comment.UserId,
             content if content is not None else comment.Content,
             editedOn if editedOn is not None else comment.EditedOn])
        self.connection.commit()
        cursor.close()

    """
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        Check Methods
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    """

    def checkUserExists(self, userId: int) -> bool:
        """
        Checks if a user exists in the database.

        Args:
            userId (int): The id of the user to check.

        Returns:
            True if the user exists, False otherwise.
        """
        self.logger.info(f"Checking if user '{userId}' exists in the database.")

        # Check if the user exists
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT Id FROM Users WHERE Id = ?;", [userId])
        user: User = cursor.fetchone()
        cursor.close()

        return user is not None

    def checkUserEmailExists(self, email: str) -> bool:
        """
        Checks if a user exists in the database.

        Args:
            email (str): The email of the user to check.

        Returns:
            True if the user exists, False otherwise.
        """
        self.logger.info(f"Checking if user '{email}' exists in the database.")

        # Check if the user exists
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT Id FROM Users WHERE Email = ?;", [email])
        user: User = cursor.fetchone()
        cursor.close()

        return user is not None

    def checkPostExists(self, postId: int) -> bool:
        """
        Checks if a post exists in the database.

        Args:
            postId (int): The id of the post to check.

        Returns:
            True if the post exists, False otherwise.
        """
        self.logger.info(f"Checking if post '{postId}' exists in the database.")

        # Check if the post exists
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT Id FROM Posts WHERE Id = ?;", [postId])
        post: Post = cursor.fetchone()
        cursor.close()

        return post is not None

    def checkTagExists(self, tagId: int) -> bool:
        """
        Checks if a tag exists in the database.

        Args:
            tagId (int): The id of the tag to check.

        Returns:
            True if the tag exists, False otherwise.
        """
        self.logger.info(f"Checking if tag '{tagId}' exists in the database.")

        # Check if the tag exists
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT Id FROM Tags WHERE Id = ?;", [tagId])
        tag: Tag = cursor.fetchone()
        cursor.close()

        return tag is not None

    def checkCommentExists(self, commentId: int) -> bool:
        """
        Checks if a comment exists in the database.

        Args:
            commentId (int): The id of the comment to check.

        Returns:
            True if the comment exists, False otherwise.
        """
        self.logger.info(f"Checking if comment '{commentId}' exists in the database.")

        # Check if the comment exists
        cursor: Cursor = self.connection.cursor()
        cursor.execute("SELECT Id FROM Comments WHERE Id = ?;", [commentId])
        comment: Comment = cursor.fetchone()
        cursor.close()

        return comment is not None


