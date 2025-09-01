"""
Genetic crossover algorithms for Darwin simulation.
"""

import random
from .dna import PreyGenome, PredatorGenome


def blend(a: float, b: float, alpha: float) -> float:
    """Blend two values using linear interpolation."""
    return a * (1 - alpha) + b * alpha


def crossover_prey(p1: PreyGenome, p2: PreyGenome, rate: float) -> PreyGenome:
    """Perform crossover between two prey genomes."""
    if random.random() > rate:
        return random.choice([p1, p2])
    
    t = random.random()
    return PreyGenome(
        speed=blend(p1.speed, p2.speed, t),
        vision=blend(p1.vision, p2.vision, t),
        stamina=blend(p1.stamina, p2.stamina, t),
        resistance=blend(p1.resistance, p2.resistance, t),
    )


def crossover_pred(a: PredatorGenome, b: PredatorGenome, rate: float) -> PredatorGenome:
    """Perform crossover between two predator genomes."""
    if random.random() > rate:
        return random.choice([a, b])
    
    t = random.random()
    return PredatorGenome(
        speed=blend(a.speed, b.speed, t),
        vision=blend(a.vision, b.vision, t),
        stamina=blend(a.stamina, b.stamina, t),
        strength=blend(a.strength, b.strength, t),
    )
