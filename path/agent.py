"""Agent class for the pathfinding algorithm."""

from path import const
from path.elements import Element


class Agent(Element):
    """Agent class."""

    def __init__(self):
        """Initialize the agent."""
        super().__init__(movable=True)

    def __str__(self):
        """Return a string representation of the agent.

        Returns:
            str: The string representation of the agent.
        """
        return 'A'

    def to_float(self):
        """Return the agent as a float.

        Returns:
            float: The agent as a float.
        """
        return const.AGENT_FLOAT
