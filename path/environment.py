"""OpenAI Gym environment for pathfinding."""

import gym
import numpy as np

from path.agent import Agent
from path.elements import Goal, Obstacle
from path.grid import Grid


class Environment(gym.Env):
    """OpenAI Gym environment for pathfinding."""

    def __init__(self, size: tuple):
        """Initialize the environment.

        Args:
            size (tuple): The size of the grid.
        """
        self.rows = size[0]
        self.cols = size[1]

        # action space of 4
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(
            low=0,
            high=1,
            shape=(self.rows, self.cols),
            dtype=np.float32,
        )
        self.reward_range = (-1, 1)

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
            reward = 1
        if self.agent.cell == prev_cell:
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
        for _ in range(3):
            self.gr.place_random(Obstacle())

        self.goal = Goal()
        self.agent = Agent()

        # goal should be placed first
        self.gr.place_random(self.goal)
        self.gr.place_random(self.agent)
        return self.gr.as_float()

    def render(self):
        """Render the environment."""
        print(self.gr)
