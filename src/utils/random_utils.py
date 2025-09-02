"""
Random number generation utilities for Darwin simulation.
"""

import random
from typing import List, TypeVar

T = TypeVar("T")


def random_choice(items: List[T]) -> T:
    """Choose a random item from a list."""
    return random.choice(items)


def random_sample(items: List[T], k: int) -> List[T]:
    """Sample k random items from a list without replacement."""
    return random.sample(items, k)


def random_gaussian(mu: float = 0.0, sigma: float = 1.0) -> float:
    """Generate a random number from a Gaussian distribution."""
    return random.gauss(mu, sigma)


def random_uniform(a: float = 0.0, b: float = 1.0) -> float:
    """Generate a random number from a uniform distribution."""
    return random.uniform(a, b)
