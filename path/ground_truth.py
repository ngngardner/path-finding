""""Find the ground truth experiences for the generated environment."""

from copy import deepcopy

import numpy as np
from beartype import beartype
from scipy.sparse.csgraph import dijkstra

from path import const
from path.environment import Environment
from path.grid import Grid


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


def get_path(predecessors, start, goal):
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
def get_ground_truth(env: Environment):
    """Return the ground truth of the environment as a series of experiences.

    Args:
        env (Environment): The environment.

    Returns:
        list: The ground truth of the environment as a series of experiences.
    """
    experiences = []
    temp = deepcopy(env)
    cols = temp.gr.size[1]

    # convert grid to graph
    adj_matrix = adjacency_matrix(temp.gr)

    # run dijkstras's algorithm until shortest path is found
    start = temp.agent.cell.location
    goal = temp.goal.cell.location

    # convert start and goal cells to adj matrix indices
    start_idx = loc_to_idx(start[0], start[1], cols)
    goal_idx = loc_to_idx(goal[0], goal[1], cols)

    # run dijkstras's algorithm
    _, predecessors = dijkstra(
        adj_matrix,
        directed=False,
        indices=start_idx,
        return_predecessors=True,
    )

    # get shortest path as a series of correct actions
    path = get_path(predecessors, start_idx, goal_idx)
    actions = path_to_actions(path, cols)
    print([const.ACTION_MAP_REV[action] for action in actions])

    # run actions on environment
    for action in actions:
        experiences.append(temp.step(action))
        temp.render()
        print('====================')

    return experiences


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
                    matrix[current_cell_idx, cell_idx] = 1
                # down
                if row < rows and grid[row + 1, col].movable:
                    cell_idx = loc_to_idx(row + 1, col, cols)
                    matrix[current_cell_idx, cell_idx] = 1
                # left
                if col > 0 and grid[row, col - 1].movable:
                    cell_idx = loc_to_idx(row, col - 1, cols)
                    matrix[current_cell_idx, cell_idx] = 1
                # right
                if col < cols and grid[row, col + 1].movable:
                    cell_idx = loc_to_idx(row, col + 1, cols)
                    matrix[current_cell_idx, cell_idx] = 1

    return matrix
