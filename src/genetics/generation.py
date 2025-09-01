"""
Genome generation utilities for Darwin simulation.
"""

import random
from .dna import PreyGenome, PredatorGenome


def random_prey(params) -> PreyGenome:
    """Generate a random prey genome within parameter bounds."""
    return PreyGenome(
        speed=random.uniform(params.speed_min, params.speed_max),
        vision=random.uniform(params.vision_min, params.vision_max),
        stamina=random.uniform(params.stamina_min, params.stamina_max),
        resistance=random.uniform(params.resist_min, params.resist_max),
    )


def random_pred(params) -> PredatorGenome:
    """Generate a random predator genome within parameter bounds."""
    return PredatorGenome(
        speed=random.uniform(params.speed_min, params.speed_max),
        vision=random.uniform(params.vision_min, params.vision_max),
        stamina=random.uniform(params.stamina_min, params.stamina_max),
        strength=random.uniform(params.strength_min, params.strength_max),
    )
