"""
Selection algorithms for genetic algorithms in Darwin simulation.
"""

import random
from typing import List, TypeVar

T = TypeVar("T")


def tournament_select(population: List[T], fitness: List[float], k: int) -> T:
    """
    Perform tournament selection to choose the best individual
    from k random candidates.

    Args:
        population: List of genomes
        fitness: List of fitness values (same length as population)
        k: Tournament size

    Returns:
        Selected genome
    """
    best_i = None
    n = len(population)

    for _ in range(k):
        i = random.randrange(n)
        if best_i is None or fitness[i] > fitness[best_i]:
            best_i = i

    return population[best_i]
