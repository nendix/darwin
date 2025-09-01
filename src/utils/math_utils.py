"""
Mathematical utility functions for Darwin simulation.
"""

import math
from typing import Tuple


def clamp(v: float, lo: float, hi: float) -> float:
    """Clamp a value between min and max bounds."""
    return max(lo, min(hi, v))


def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Calculate Euclidean distance between two points."""
    return math.hypot(a[0] - b[0], a[1] - b[1])


def norm(x: float, y: float) -> float:
    """Calculate the norm (magnitude) of a 2D vector."""
    return math.hypot(x, y)


def normalize(x: float, y: float) -> Tuple[float, float]:
    """Normalize a 2D vector to unit length."""
    n = norm(x, y)
    if n == 0:
        return (0.0, 0.0)
    return (x / n, y / n)
