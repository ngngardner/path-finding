""""Find the ground truth experiences for the generated environment."""

import numpy as np
from beartype import beartype

from path import const
from path.grid import Grid

UNREACHABLE = -9999


@beartype
def loc_to_idx(row: int, col: int, cols: int) -> int:
    """Convert a row and column to an index to a flattened array.

    Args:
        row (int): The row.
        col (int): The column.
        cols (int): The number of cols.

    Returns:
        int: The index.
    """
    return row * cols + col


def get_path(predecessors: np.ndarray, start: int, goal: int) -> list:
    """"Get the path from the predecessors array.

    Args:
        predecessors (np.ndarray): The predecessors array.
        start (int): The start index.
        goal (int): The goal index.

    Returns:
        list: The path.

    Raises:
        ValueError: If the goal is unreachable.
    """
    if predecessors[goal] == UNREACHABLE:
        raise ValueError('No path to goal.')
    res = []
    current = goal
    while current != start:
        res.append(current)
        current = predecessors[current]

    res.append(start)
    res.reverse()
    return res


def path_to_actions(path, cols: int):
    actions = []
    for point in range(len(path)-1):
        diff = path[point+1] - path[point]
        # move up
        if diff == -cols:
            actions.append(const.ACTION_MAP['up'])
        # move down
        elif diff == cols:
            actions.append(const.ACTION_MAP['down'])
        # move left
        elif diff == -1:
            actions.append(const.ACTION_MAP['left'])
        # move right
        elif diff == 1:
            actions.append(const.ACTION_MAP['right'])
    return actions


@beartype
def adjacency_matrix(grid: Grid) -> np.ndarray:
    """Return the adjacency matrix of the grid.

    Args:
        grid (Grid): The grid.

    Returns:
        np.ndarray: The adjacency matrix of the grid.
    """
    rows, cols = grid.size
    matrix = np.zeros((rows*cols, rows*cols))
    for row in range(0, rows):
        for col in range(0, cols):
            if grid[row, col].movable:
                current_cell_idx = loc_to_idx(row, col, cols)
                # up
                if row > 0 and grid[row - 1, col].movable:
                    cell_idx = loc_to_idx(row - 1, col, cols)
                    cost = grid[row - 1, col].move_cost
                    matrix[current_cell_idx, cell_idx] = cost
                # down
                if row < rows and grid[row + 1, col].movable:
                    cell_idx = loc_to_idx(row + 1, col, cols)
                    cost = grid[row + 1, col].move_cost
                    matrix[current_cell_idx, cell_idx] = cost
                # left
                if col > 0 and grid[row, col - 1].movable:
                    cell_idx = loc_to_idx(row, col - 1, cols)
                    cost = grid[row, col - 1].move_cost
                    matrix[current_cell_idx, cell_idx] = cost
                # right
                if col < cols and grid[row, col + 1].movable:
                    cell_idx = loc_to_idx(row, col + 1, cols)
                    cost = grid[row, col + 1].move_cost
                    matrix[current_cell_idx, cell_idx] = cost

    return matrix
