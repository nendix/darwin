import math
import random
from typing import Tuple


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def dist(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def norm(x: float, y: float) -> float:
    return math.hypot(x, y)


def normalize(x: float, y: float) -> Tuple[float, float]:
    n = norm(x, y)
    if n == 0:
        return (0.0, 0.0)
    return (x / n, y / n)


def rand_pos(w: int, h: int) -> Tuple[float, float]:
    return (random.uniform(0, w), random.uniform(0, h))


def wrap(x: float, y: float, w: int, h: int) -> Tuple[float, float]:
    if x < 0:
        x += w
    if x >= w:
        x -= w
    if y < 0:
        y += h
    if y >= h:
        y -= h
    return (x, y)
