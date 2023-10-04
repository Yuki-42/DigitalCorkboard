# Database

This page details all there is to know about the database system that the project uses.

## Database structure

The database is structured in such a way that, should any post be deleted, all comments on that post will be deleted as 
well. This is done by setting the `ON DELETE CASCADE` option on the foreign key constraint of the `Comments` table.

### Tables

The database has several tables, each of which is described below.
- `Users`
- `Posts`
- `Tags`
- `Comments`
- `PostTags`

#### Users

The `Users` table contains all the information about the users of the system.

| Column name | Type       | Nullable | Additional Data | Description                   |
|-------------|------------|----------|-----------------|-------------------------------|
| `Id`        | `Int`      | No       | Autoincrement   | The unique ID of the user.    |
| `FirstName` | `Text`     | No       |                 | The username of the user.     |
| `LastName`  | `Text`     | No       |                 | The username of the user.     |
| `Email`     | `Text`     | No       | Unique          | The email of the user.        |
| `Password`  | `Text`     | No       |                 | The password of the user.     |
| `Admin`     | `Bool`     | No       | Default false   | Whether the user is an admin. |
| `Bio`       | `Text`     | Yes      |                 | The bio of the user.          |
| `AddedOn`   | `DateTime` | No       |                 | The date the user joined.     |

#### Posts

The `Posts` table contains all the information about the posts of the system.

| Column name | Type       | Nullable | Additional Data | Description                                       |
|-------------|------------|----------|-----------------|---------------------------------------------------|
| `Id`        | `Int`      | No       | Autoincrement   | The unique ID of the post.                        |
| `CreatorId` | `Int`      | No       |                 | The ID of the creator.                            |
| `Title`     | `Text`     | No       |                 | The title of the post.                            |
| `Content`   | `Text`     | No       |                 | The content of the post.                          |
| `AddedOn`   | `DateTime` | No       |                 | The date the post was made.                       |
| `ExpiresOn` | `DateTime` | Yes      |                 | The date the post expires.                        |

#### Tags

The `Tags` table contains all the information about the tags of the system.

| Column name   | Type       | Nullable | Additional Data | Description                 |
|---------------|------------|----------|-----------------|-----------------------------|
| `Id`          | `Int`      | No       | Autoincrement   | The unique ID of the tag.   |
| `Name`        | `Text`     | No       |                 | The name of the tag.        |
| `Description` | `Text`     | Yes      |                 | The description of the tag. |
| `Colour`      | `Text`     | No       |                 | The RGB colour of the tag.  |
| `AddedOn`     | `DateTime` | No       |                 | The date the tag was added. |

#### Comments

The `Comments` table contains all the information about every single comment in the system. 

| Column name | Type       | Nullable | Additional Data | Description                                       |
|-------------|------------|----------|-----------------|---------------------------------------------------|
| `Id`        | `Int`      | No       | Autoincrement   | The unique ID of the comment.                     |
| `PostId`    | `Int`      | No       |                 | The ID of the post the comment is on.             |
| `UserId`    | `Int`      | No       |                 | The ID of the user who made the comment.          |
| `Content`   | `Text`     | No       |                 | The content of the comment.                       |
| `AddedOn`   | `DateTime` | No       |                 | The date the comment was made.                    |
| `EditedOn`  | `DateTime` | Yes      |                 | The date the comment was last edited.             |

#### PostTags

The `PostTags` table is used to relate posts to tags. It contains the IDs of the posts and tags that are related.

| Column name | Type       | Nullable | Additional Data | Description                                       |
|-------------|------------|----------|-----------------|---------------------------------------------------|
| `PostId`    | `Int`      | No       |                 | The ID of the post.                               |
| `TagId`     | `Int`      | No       |                 | The ID of the tag.                                |

### Relationships

The database has several relationships, each of which is described below.

#### Users to Posts

The `Users` table has a one-to-many relationship with the `Posts` table. This means that a user can have many posts,
but a post can only have one user.

#### Posts to Comments

The `Posts` table has a one-to-many relationship with the `Comments` table. This means that a post can have many
comments, but a comment can only have one post.

#### Users to Comments

The `Users` table has a one-to-many relationship with the `Comments` table. This means that a user can have many
comments, but a comment can only have one user.

#### Posts to Tags

The `Posts` table has a many-to-many relationship with the `Tags` table. This means that a post can have many tags,
and a tag can have many posts. This is done by using the `PostTags` table. This table contains the IDs of the posts
and tags that are related.

### Creating the database

The database can be created by running the following command:

```sqlite
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
    FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
    FOREIGN KEY (UserId) REFERENCES Users(Id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PostTags (
    PostId INTEGER NOT NULL,
    TagId INTEGER NOT NULL,
    FOREIGN KEY (PostId) REFERENCES Posts(Id) ON DELETE CASCADE,
    FOREIGN KEY (TagId) REFERENCES Tags(Id) ON DELETE CASCADE
);
```

## Database access

The database can be accessed using the `Database` class. This class is located in the `internals` package. 

### Methods

The `Database` class has several methods, each of which is described below.

#### Miscellaneous methods

This section details all miscellaneous methods.

##### `__init__()`

The `__init__()` method is the constructor for the `Database` class. It takes no arguments. It also runs the 
`_checkTablesExist()` method.

##### `__del__()`

The `__del__()` method is the destructor for the `Database` class. It takes no arguments. It closes the connection to
the database.

##### `_checkTablesExist()`

The `_checkTablesExist()` method checks if the tables exist in the database. It takes no arguments. It returns nothing.
It checks that the database contains all the correct tables, and if it encounters a missing table, it creates it.

#### Properties

This section details all properties. Properties are used instead of `getAll()` methods to make it easier for the
developers to quickly and concisely access needed data from the database in a readable fashion. There should be
absolutely no use of methods that get all data from the database in the rest of the code. 

##### `users`

The `users` property gets all users from the database. It returns a list of `User` objects.

##### `posts`

The `posts` property gets all posts from the database. It returns a list of `Post` objects.

##### `tags`

The `tags` property gets all tags from the database. It returns a list of `Tag` objects.

##### `comments`

The `comments` property gets all comments from the database. It returns a list of `Comment` objects.

##### `postTags`

The `postTags` property gets all post tags from the database. It returns a list of tuples, each of which contains the

#### Add methods

This section details all methods that add whole rows to the database.

##### `addUser`

The `addUser()` method adds a user to the database. It takes the following arguments:
- `firstName`: The first name of the user.
- `lastName`: The last name of the user.
- `email`: The email of the user.
- `password`: The password of the user.

The method returns the ID of the user that was added.

##### `addPost`

The `addPost()` method adds a post to the database. It takes the following arguments:
- `creatorId`: The ID of the creator of the post.
- `title`: The title of the post.
- `content`: The content of the post.
- `expiresOn`: The date the post expires.
- `tags`: The tags of the post. This is a list of integers representing the IDs of the tags.

The method returns the ID of the post that was added.

##### `addTag`

The `addTag()` method adds a tag to the database. It takes the following arguments:

- `name`: The name of the tag.
- `description`: The description of the tag.
- `colour`: The colour of the tag.

The method returns the ID of the tag that was added.

##### `addComment`

The `addComment()` method adds a comment to the database. It takes the following arguments:

- `postId`: The ID of the post the comment is on.
- `userId`: The ID of the user who made the comment.
- `content`: The content of the comment.

The method returns the ID of the comment that was added.

#### Misnomer Add Methods

This section details all methods that add data to the database, without adding a whole row. They are called misnomer add
methods because they do not actually add a row to the database, but rather add data to an existing row. It would be 
unwise to rename them, however, as their naming makes sense in the context of the rest of the code.

##### `addPostTag`

The `addPostTag()` method adds a tag to a post. It takes the following arguments:

- `postId`: The ID of the post.
- `tagId`: The ID of the tag.

The method returns nothing.

#### Remove methods

This section details all methods that remove whole rows from the database.

##### `removeUser`

The `removeUser()` method removes a user from the database. When removing a user, all posts and comments made by that
user are also removed. It takes the following arguments:

- `userId`: The ID of the user.

The method returns nothing.

##### `removePost`

The `removePost()` method removes a post from the database. When removing a post, all comments on that post are also
removed and all tags on that post are also removed. It takes the following arguments:

- `postId`: The ID of the post.

The method returns nothing.

##### `removeTag`

The `removeTag()` method removes a tag from the database. When removing a tag, all posts with that tag are also removed.
It takes the following arguments:

- `tagId`: The ID of the tag.

The method returns nothing.

##### `removeComment`

The `removeComment()` method removes a comment from the database. It takes the following arguments:

- `commentId`: The ID of the comment.

The method returns nothing.

#### Misnomer Remove Methods

This section details all methods that remove data from the database, without removing a whole row. They are called
misnomer remove methods because they do not actually remove a row from the database, but rather remove data from an
existing row. It would be unwise to rename them, however, as their naming makes sense in the context of the rest of the
code.

##### `removePostTag`

The `removePostTag()` method removes a tag from a post. It takes the following arguments:

- `postId`: The ID of the post.
- `tagId`: The ID of the tag.

The method returns nothing.

#### Modify methods

This section details all methods that modify specific fields in the database.

##### `modifyUser`

The `modifyUser()` method modifies a user in the database. The only argument required is the ID of the user. The method 
takes the following keyword arguments:

- `firstName`: The first name of the user.
- `lastName`: The last name of the user.
- `email`: The email of the user.
- `password`: The password of the user.
- `admin`: Whether the user is an admin.
- `bio`: The bio of the user.

The method returns nothing.

##### `modifyPost`

The `modifyPost()` method modifies a post in the database. The only argument required is the ID of the post. The method
takes the following keyword arguments:

- `creatorId`: The ID of the creator of the post.
- `title`: The title of the post.
- `content`: The content of the post.
- `expiresOn`: The date the post expires.
- `tags`: The tags of the post. This is a list of integers representing the IDs of the tags.

The method returns nothing.

##### `modifyTag`

The `modifyTag()` method modifies a tag in the database. The only argument required is the ID of the tag. The method
takes the following keyword arguments:

- `name`: The name of the tag.
- `description`: The description of the tag.
- `colour`: The colour of the tag.

The method returns nothing.

##### `modifyComment`

The `modifyComment()` method modifies a comment in the database. The only argument required is the ID of the comment.
The method takes the following keyword arguments:

- `postId`: The ID of the post the comment is on.
- `userId`: The ID of the user who made the comment.
- `content`: The content of the comment.
- `editedOn`: The date the comment was last edited.

The method returns nothing.

#### Check methods

This section details all methods that check if a row exists in the database.

##### `checkUserExists`

The `checkUserExists()` method checks if a user exists in the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns a boolean value.

##### `checkPostExists`

The `checkPostExists()` method checks if a post exists in the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns a boolean value.

##### `checkTagExists`

The `checkTagExists()` method checks if a tag exists in the database. It takes the following arguments:

- `tagId`: The ID of the tag.

The method returns a boolean value.

##### `checkCommentExists`

The `checkCommentExists()` method checks if a comment exists in the database. It takes the following arguments:

- `commentId`: The ID of the comment.

The method returns a boolean value.

#### Get methods

This section details all methods that get data from the database.

##### `getUserId`

The `getUserId()` method gets the ID of a user from the database. It takes the following arguments:

- `email`: The email of the user.

The method returns the ID of the user.

##### `getUser`

The `getUser()` method gets a user from the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns a `User` object.

##### `getUserName`

The `getUserName()` method gets the name of a user from the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns a tuple containing the first and last name of the user.

##### `getUserEmail`

The `getUserEmail()` method gets the email of a user from the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns the email of the user.

##### `getUserPassword`

The `getUserPassword()` method gets the password of a user from the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns the password of the user.

##### `getUserAdmin`

The `getUserAdmin()` method gets whether a user is an admin from the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns a boolean value.

##### `getUserBio`

The `getUserBio()` method gets the bio of a user from the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns the bio of the user.

##### `getUserAddedOn`

The `getUserAddedOn()` method gets the date a user joined from the database. It takes the following arguments:

- `userId`: The ID of the user.

The method returns the date the user joined.


##### `getPost`

The `getPost()` method gets a post from the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns a `Post` object.

##### `getPostCreatorId`

The `getPostCreatorId()` method gets the ID of the creator of a post from the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns the ID of the creator of the post.

##### `getPostTitle`

The `getPostTitle()` method gets the title of a post from the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns the title of the post.

##### `getPostContent`

The `getPostContent()` method gets the content of a post from the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns the content of the post.

##### `getPostAddedOn`

The `getPostAddedOn()` method gets the date a post was made from the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns the date the post was made.

##### `getPostExpiresOn`

The `getPostExpiresOn()` method gets the date a post expires from the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns the date the post expires.

##### `getTag`

The `getTag()` method gets a tag from the database. It takes the following arguments:

- `tagId`: The ID of the tag.

The method returns a `Tag` object.

##### `getTagName`

The `getTagName()` method gets the name of a tag from the database. It takes the following arguments:

- `tagId`: The ID of the tag.

The method returns the name of the tag.

##### `getTagDescription`

The `getTagDescription()` method gets the description of a tag from the database. It takes the following arguments:

- `tagId`: The ID of the tag.

The method returns the description of the tag.

##### `getTagColour`

The `getTagColour()` method gets the colour of a tag from the database. It takes the following arguments:

- `tagId`: The ID of the tag.

The method returns the colour of the tag.

##### `getTagAddedOn`

The `getTagAddedOn()` method gets the date a tag was added from the database. It takes the following arguments:

- `tagId`: The ID of the tag.

The method returns the date the tag was added.

##### `getComment`

The `getComment()` method gets a comment from the database. It takes the following arguments:

- `commentId`: The ID of the comment.

The method returns a `Comment` object.

##### `getCommentPostId`

The `getCommentPostId()` method gets the ID of the post a comment is on from the database. It takes the following

- `commentId`: The ID of the comment.

The method returns the ID of the post the comment is on.

##### `getCommentUserId`

The `getCommentUserId()` method gets the ID of the user who made a comment from the database. It takes the following

- `commentId`: The ID of the comment.

The method returns the ID of the user who made the comment.

##### `getCommentContent`

The `getCommentContent()` method gets the content of a comment from the database. It takes the following arguments:

- `commentId`: The ID of the comment.

The method returns the content of the comment.

##### `getCommentAddedOn`

The `getCommentAddedOn()` method gets the date a comment was made from the database. It takes the following arguments:

- `commentId`: The ID of the comment.

The method returns the date the comment was made.

##### `getCommentEditedOn`

The `getCommentEditedOn()` method gets the date a comment was last edited from the database. It takes the following

- `commentId`: The ID of the comment.

The method returns the date the comment was last edited.

##### `getPostTags`

The `getPostTags()` method gets the tags of a post from the database. It takes the following arguments:

- `postId`: The ID of the post.

The method returns the list of `tagId`s associated with the post.

#### Cryptographic methods

This section details all methods that use cryptography. They are mainly used for password handling.

##### `attemptLogin`

The `attemptLogin()` method attempts to log a user in. It takes the following arguments:

- `email`: The email of the user.
- `password`: The password of the user.

The method returns a boolean value indicating whether the login was successful.

### Custom Datatypes

The database makes use of several custom datatypes, each of which is described below, to represent rows in the database.

This is done to make it easier for the developers to quickly and concisely access needed data from the database in a 
readable fashion. 

#### User

The `User` datatype represents a row in the `Users` table. It contains the following attributes:
- `id`: The ID of the user.
- `firstName`: The first name of the user.
- `lastName`: The last name of the user.
- `email`: The email of the user.
- `password`: The password of the user.
- `admin`: Whether the user is an admin.
- `bio`: The bio of the user.
- `addedOn`: The date the user joined.

#### Post

The `Post` datatype represents a row in the `Posts` table. It contains the following attributes:

- `id`: The ID of the post.
- `creatorId`: The ID of the creator of the post.
- `title`: The title of the post.
- `content`: The content of the post.
- `addedOn`: The date the post was made.
- `expiresOn`: The date the post expires.

#### Tag

The `Tag` datatype represents a row in the `Tags` table. It contains the following attributes:

- `id`: The ID of the tag.
- `name`: The name of the tag.
- `description`: The description of the tag.
- `colour`: The colour of the tag.
- `addedOn`: The date the tag was added.

#### Comment

The `Comment` datatype represents a row in the `Comments` table. It contains the following attributes:

- `id`: The ID of the comment.
- `postId`: The ID of the post the comment is on.
- `userId`: The ID of the user who made the comment.
- `content`: The content of the comment.
- `addedOn`: The date the comment was made.
- `editedOn`: The date the comment was last edited.
