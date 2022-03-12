"""Module for the grid."""

import numpy as np
from beartype import beartype

from path.cell import Cell
from path.elements import Element


class Grid(object):
    """Grid class."""

    @beartype
    def __init__(self, size: tuple):
        """Initialize the grid.

        Args:
            size (tuple): The size of the grid.
        """
        self.size = size
        self.grid = np.zeros(size, dtype=Cell)
        for row in range(size[0]):
            for col in range(size[1]):
                self.grid[row, col] = Cell(row, col)

    @beartype
    def move(self, element: Element, dest: tuple) -> bool:
        """Move an element to a new cell.

        Args:
            element (Element): The element to move.
            dest (tuple): The destination cell.

        Returns:
            bool: True if the element was moved, False otherwise.
        """
        cell = self.grid[dest]
        if cell.movable:
            element.move(cell)
            return True
        return False

    @beartype
    def place(self, element: Element, dest: tuple) -> bool:
        """Place an element in a cell. Uses move().

        Args:
            element (Element): The element to place.
            dest (tuple): The destination cell.

        Returns:
            bool: True if the element was placed, False otherwise.
        """
        return self.move(element, dest)

    @beartype
    def get_random(self) -> tuple:
        """Return a random row and column inside the grid.

        Returns:
            tuple: A random row and column inside the grid.
        """
        return (
            np.random.randint(self.size[0]),
            np.random.randint(self.size[1]),
        )

    @beartype
    def get_random_movable(self) -> tuple:
        """Get a random movable cell.

        Returns:
            tuple: A random movable cell.
        """
        while True:
            row, col = self.get_random()
            cell = self.grid[row, col]
            if cell.movable and not cell.is_goal:
                return row, col

    @beartype
    def place_random(self, element: Element):
        """Place an element at a random movable cell.

        Args:
            element (Element): The element to place.
        """
        self.place(element, self.get_random_movable())

    def __str__(self):
        """Return a string representation of the grid.

        Returns:
            str: The string representation of the grid.
        """
        return '\n'.join(
            ''.join(str(cell) for cell in row)
            for row in self.grid
        )

    def __getitem__(self, key: tuple) -> Cell:
        """Get the cell at a given position.

        Args:
            key (tuple): The position of the cell.

        Returns:
            Cell: The cell at the given position.
        """
        return self.grid[key]

    def as_float(self) -> np.ndarray:
        """Return the grid as a float.

        Returns:
            np.ndarray: The grid as a float.
        """
        return np.array(
            [[cell.to_float() for cell in row] for row in self.grid],
            dtype=np.float32,
        )
