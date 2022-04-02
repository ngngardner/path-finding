"""Constants for the path package."""

# default cost of moving into a cell
DEFAULT_COST = 1.0

GOAL_FLOAT = 0.1
AGENT_FLOAT = 0.2
OBSTACLE_FLOAT = 0.9
# TODO: if we change the cost of a trap, the representation should change
TRAP_FLOAT = 0.4

ACTION_MAP = {
    'up': 0,
    'down': 1,
    'left': 2,
    'right': 3,
}
ACTION_MAP_REV = {vl: key for key, vl in ACTION_MAP.items()}
