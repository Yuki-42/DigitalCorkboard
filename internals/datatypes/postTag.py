"""
Contains the PostTag class which is used to represent a post-tag pair in the database.
"""


class PostTag:
    """
    Represents a post-tag pair in the database.
    """

    # Type hinting
    PostId: int
    TagId: int

    def __init__(self, postTag: tuple[int, int]):
        """
        Initializes a new instance of the PostTag class.

        Args:
            postTag (tuple[int, int]): The post-tag pair tuple from the database.
        """

        self.PostId = postTag[0]
        self.TagId = postTag[1]

