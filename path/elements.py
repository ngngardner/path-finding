"""Module for grid elements."""

from path.cell import Cell


class Element(object):
    """Base grid element class."""

    def __init__(self, movable: bool, cell: Cell | None = None):
        """Initialize the element.

        Args:
            movable (bool): Whether element can be moved into.
            cell (Cell | None): The cell which contains the element.
        """
        self.movable = movable
        self.cell = cell

    @property
    def is_goal(self) -> bool:
        """Return if the element is a goal. Default is False.

        Returns:
            bool: True if the element is a goal, False otherwise.
        """
        return False

    def move(self, cell: Cell) -> None:
        """Move the element to a new cell.

        Args:
            cell (Cell): The cell to move to.
        """
        # element has yet to be assigned to a cell
        if self.cell is None:
            self.cell = cell
            self.cell.push(self)
        # element has been assigned to a cell
        else:
            self.cell.pop(self)
            self.cell = cell
            self.cell.push(self)


class Obstacle(Element):
    """Obstacle element class."""

    def __init__(self):
        """Initialize the obstacle."""
        super().__init__(movable=False)

    def __str__(self):
        """Return a string representation of the obstacle.

        Returns:
            str: The string representation of the obstacle.
        """
        return '#'


class Goal(Element):
    """Goal element class."""
    def __init__(self):
        """Initialize the goal."""
        super().__init__(movable=True)

    @property
    def is_goal(self) -> bool:
        """Return if the element is a goal. Default is True.

        Returns:
            bool: True if the element is a goal, False otherwise.
        """
        return True

    def __str__(self):
        """Return a string representation of the goal.

        Returns:
            str: The string representation of the goal.
        """
        return 'G'
