"""Constants for the path package."""

GOAL_FLOAT = 0.1
AGENT_FLOAT = 0.2
OBSTACLE_FLOAT = 0.3

ACTION_MAP = {
    'up': 0,
    'down': 1,
    'left': 2,
    'right': 3,
}
ACTION_MAP_REV = {vl: key for key, vl in ACTION_MAP.items()}
