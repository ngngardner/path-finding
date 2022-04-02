"""OpenAI Gym environment for pathfinding."""
from copy import deepcopy

import gym
import numpy as np
from beartype import beartype
from scipy.sparse.csgraph import dijkstra

from path import const
from path.agent import Agent
from path.elements import Goal, Obstacle, Trap
from path.grid import Grid
from path.ground_truth import adjacency_matrix, get_path, loc_to_idx, path_to_actions


class Environment(gym.Env):
    """OpenAI Gym environment for pathfinding."""

    def __init__(self, size: tuple = (8, 8)):
        """Initialize the environment.

        Args:
            size (tuple): The size of the grid.
        """
        self.rows = size[0]
        self.cols = size[1]
        self.ground_truth = None

        # action space of 4
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(
            low=0,
            high=1,
            shape=(self.rows, self.cols),
            dtype=np.float32,
        )
        self.reward_range = (-10, 10)

        self.gr = Grid((self.rows, self.cols))

    def step(self, action: int) -> tuple[np.ndarray, float, bool, dict]:
        """Perform an action and return the next state, reward, and done flag.

        Args:
            action (int): The action to perform.

        Returns:
            ndarray: The next state.
            float: The reward.
            bool: True if the episode is done, False otherwise.
            dict: Additional information.
        """
        prev_cell = self.agent.cell
        done = False
        reward = 0
        agent_row, agent_col = self.agent.cell.location

        if action not in range(4):
            raise ValueError('Invalid action {}'.format(action))

        # move up
        if action == 0:
            self.gr.move(
                self.agent, (agent_row - 1, agent_col),
            )
        # move down
        elif action == 1:
            self.gr.move(
                self.agent, (agent_row + 1, agent_col),
            )
        # move left
        elif action == 2:
            self.gr.move(
                self.agent, (agent_row, agent_col - 1),
            )
        # move right
        elif action == 3:
            self.gr.move(
                self.agent, (agent_row, agent_col + 1),
            )

        # check if agent is at goal
        if self.agent.cell.is_goal:
            done = True
            reward = 10
        if self.agent.cell == prev_cell:
            reward = -10
        else:
            reward = -1

        return self.gr.as_float(), reward, done, {}

    def reset(self) -> np.ndarray:
        """Reset the environment.

        Returns:
            ndarray: The state of the environment.
        """
        self.gr = Grid((self.rows, self.cols))

        # barrier around edge of grid
        for row in range(self.rows):
            self.gr.place(Obstacle(), (row, 0))
            self.gr.place(Obstacle(), (row, self.cols - 1))
        for col in range(self.cols):
            self.gr.place(Obstacle(), (0, col))
            self.gr.place(Obstacle(), (self.rows - 1, col))

        # place random obstacles
        # for _ in range(3):
        #     self.gr.place_random(Obstacle())

        # place random traps
        # for _ in range(20):
        #     self.gr.place_random(Trap())

        self.goal = Goal()
        self.agent = Agent()

        # goal should be placed first
        self.gr.place(self.goal, (self.rows - 2, self.cols - 2))
        self.gr.place_random(self.agent)

        # regenerate if no path exists
        try:
            self.ground_truth = get_ground_truth(self, render=False)
        except ValueError as err:
            print(err)
            self.reset()
        return self.gr.as_float()

    def render(self):
        """Render the environment."""
        print(self.gr)


@beartype
def get_ground_truth(env: Environment, render: bool = True):
    """Return the ground truth of the environment as a series of experiences.

    Args:
        env (Environment): The environment.
        render (bool): Whether to render the environment.

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
    try:
        path = get_path(predecessors, start_idx, goal_idx)
    except ValueError as err:
        raise ValueError(err)
    actions = path_to_actions(path, cols)

    if render:
        print([const.ACTION_MAP_REV[action] for action in actions])

    # run actions on environment
    for action in actions:
        res = temp.step(action)
        experiences.append({
            'action': action,
            'state': res[0],
            'reward': res[1],
            'done': res[2],
        })

        if render:
            temp.render()
            print('====================')

    return experiences
