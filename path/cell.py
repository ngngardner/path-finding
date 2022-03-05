"""Grid cell module."""


class Cell(object):
    """Cell holds the elements that are in the same location in the grid."""

    def __init__(self, members: list = None):
        """Initialize the cell.

        Args:
            members (list): The list of elements in the cell.
        """
        if members is None:
            self.members = []
        else:
            self.members = members

    @property
    def movable(self):
        """Return the movable status of the cell.

        Returns:
            bool: True if the cell is movable, False otherwise.
        """
        for member in self.members:
            if not member.movable:
                return False
        return True

    def pop(self, element: object) -> object:
        """Remove an element from the cell members.

        Args:
            element (object): The element to be removed.

        Returns:
            object: The element that was removed.
        """
        return self.members.pop(element)

    def push(self, element: object):
        """Add an element to the cell members.

        Args:
            element (object): The element to be added.
        """
        self.members.append(element)

    def __str__(self):
        """Return a string representation of the cell.

        Returns:
            str: The string representation of the cell.
        """
        if self.members:
            return '|{0}|'.format(
                ''.join(str(member) for member in self.members),
            )
        return '|_|'
