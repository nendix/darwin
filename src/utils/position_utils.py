"""
Position and coordinate utilities for Darwin simulation.
"""

import random
from typing import Tuple


def rand_pos(w: int, h: int) -> Tuple[float, float]:
    """Generate a random position within the given bounds."""
    return (random.uniform(0, w), random.uniform(0, h))


def clamp_to_bounds(
    x: float, y: float, w: int, h: int, radius: float = 5.0
) -> Tuple[float, float]:
    """Clamp coordinates to stay within world bounds (no wrapping)."""
    x = max(radius, min(w - radius, x))
    y = max(radius, min(h - radius, y))
    return (x, y)


def check_collision(
    agent1_pos: Tuple[float, float],
    agent2_pos: Tuple[float, float],
    min_distance: float = 8.0,
) -> bool:
    """Check if two agents are too close to each other."""
    dx = agent1_pos[0] - agent2_pos[0]
    dy = agent1_pos[1] - agent2_pos[1]
    distance = (dx * dx + dy * dy) ** 0.5
    return distance < min_distance


def resolve_collision(
    agent_pos: Tuple[float, float],
    other_pos: Tuple[float, float],
    min_distance: float = 8.0,
) -> Tuple[float, float]:
    """Move agent away from collision with another agent."""
    dx = agent_pos[0] - other_pos[0]
    dy = agent_pos[1] - other_pos[1]
    distance = (dx * dx + dy * dy) ** 0.5

    if distance < min_distance and distance > 0:
        # Push agent away to maintain minimum distance
        push_factor = (min_distance - distance) / distance
        new_x = agent_pos[0] + dx * push_factor * 0.5
        new_y = agent_pos[1] + dy * push_factor * 0.5
        return (new_x, new_y)

    return agent_pos
