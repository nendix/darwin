"""
Genetic mutation algorithms for Darwin simulation.
"""

import random
import numpy as np
from .dna import PreyGenome, PredatorGenome
from ..utils.math_utils import clamp


def mut(val: float, std: float, lo: float, hi: float, rate: float) -> float:
    """Apply mutation to a single trait value."""
    if random.random() < rate:
        val = float(np.random.normal(val, std * (hi - lo)))
    return clamp(val, lo, hi)


def mutate_prey(g: PreyGenome, params) -> PreyGenome:
    """Apply mutation to a prey genome."""
    return PreyGenome(
        speed=mut(g.speed, params.mutation_std, params.speed_min, params.speed_max, params.mutation_rate),
        vision=mut(g.vision, params.mutation_std, params.vision_min, params.vision_max, params.mutation_rate),
        stamina=mut(g.stamina, params.mutation_std, params.stamina_min, params.stamina_max, params.mutation_rate),
        resistance=mut(g.resistance, params.mutation_std, params.resist_min, params.resist_max, params.mutation_rate),
    )


def mutate_pred(g: PredatorGenome, params) -> PredatorGenome:
    """Apply mutation to a predator genome."""
    return PredatorGenome(
        speed=mut(g.speed, params.mutation_std, params.speed_min, params.speed_max, params.mutation_rate),
        vision=mut(g.vision, params.mutation_std, params.vision_min, params.vision_max, params.mutation_rate),
        stamina=mut(g.stamina, params.mutation_std, params.stamina_min, params.stamina_max, params.mutation_rate),
        strength=mut(g.strength, params.mutation_std, params.strength_min, params.strength_max, params.mutation_rate),
    )
