"""Grid cell module."""

from beartype import beartype

from path import const

HIGH_COST = 9999


class Cell(object):
    """Cell holds the elements that are in the same location in the grid."""

    def __init__(self, row: int, col: int, members: list = None):
        """Initialize the cell.

        Args:
            row (int): The row of the cell.
            col (int): The column of the cell.
            members (list): The list of elements in the cell.
        """
        self.row = row
        self.col = col
        if members is None:
            self.members = []
        else:
            self.members = members

    @property
    def location(self) -> tuple:
        """Return the location of the cell.

        Returns:
            tuple: The location of the cell.
        """
        return self.row, self.col

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

    @property
    def move_cost(self) -> float:
        """Return the cost of moving into the cell.

        Returns:
            float: The cost of moving into the cell.
        """
        if not self.movable:
            return HIGH_COST

        for member in self.members:
            if member.move_cost != const.DEFAULT_COST:
                return member.move_cost
        return const.DEFAULT_COST

    @property
    def is_goal(self):
        """Return if the cell is a goal.

        Returns:
            bool: True if the cell is a goal, False otherwise.
        """
        for member in self.members:
            if member.is_goal:
                return True
        return False

    @property
    def is_empty(self):
        """Return if the cell is empty.

        Returns:
            bool: True if the cell is empty, False otherwise.
        """
        return len(self.members) == 0

    @beartype
    def pop(self, element: object) -> object:
        """Remove an element from the cell members.

        Args:
            element (object): The element to be removed.

        Returns:
            object: The element that was removed.
        """
        self.members.remove(element)
        return element

    @beartype
    def push(self, element: object):
        """Add an element to the cell members.

        Args:
            element (object): The element to be added.
        """
        self.members.append(element)

    @beartype
    def __str__(self) -> str:
        """Return a string representation of the cell.

        Returns:
            str: The string representation of the cell.
        """
        if self.members:
            return '|{0}|'.format(
                ''.join(str(member) for member in self.members),
            )
        return '|_|'

    @beartype
    def to_float(self) -> float:
        """Return the cell as a float.

        Returns:
            float: The cell as a float.
        """
        if self.members:
            return sum(member.to_float() for member in self.members)
        return float(0)
