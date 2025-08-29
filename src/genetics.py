from dataclasses import dataclass
import random
import numpy as np
from .utils import clamp


@dataclass
class PreyGenome:
    speed: float
    vision: float
    stamina: float  # stamina is max energy
    resistance: float


@dataclass
class PredatorGenome:
    speed: float
    vision: float
    stamina: float  # stamina is max energy
    strength: float


def random_prey(params):
    return PreyGenome(
        speed=random.uniform(params.speed_min, params.speed_max),
        vision=random.uniform(params.vision_min, params.vision_max),
        stamina=random.uniform(params.stamina_min, params.stamina_max),
        resistance=random.uniform(params.resist_min, params.resist_max),
    )


def random_pred(params):
    return PredatorGenome(
        speed=random.uniform(params.speed_min, params.speed_max),
        vision=random.uniform(params.vision_min, params.vision_max),
        stamina=random.uniform(params.stamina_min, params.stamina_max),
        strength=random.uniform(params.strength_min, params.strength_max),
    )


def blend(a: float, b: float, alpha: float) -> float:
    return a * (1 - alpha) + b * alpha


def crossover_prey(p1: PreyGenome, p2: PreyGenome, rate: float):
    if random.random() > rate:
        return random.choice([p1, p2])
    t = random.random()
    return PreyGenome(
        speed=blend(p1.speed, p2.speed, t),
        vision=blend(p1.vision, p2.vision, t),
        stamina=blend(p1.stamina, p2.stamina, t),
        resistance=blend(p1.resistance, p2.resistance, t),
    )


def crossover_pred(a: PredatorGenome, b: PredatorGenome, rate: float):
    if random.random() > rate:
        return random.choice([a, b])
    t = random.random()
    return PredatorGenome(
        speed=blend(a.speed, b.speed, t),
        vision=blend(a.vision, b.vision, t),
        stamina=blend(a.stamina, b.stamina, t),
        strength=blend(a.strength, b.strength, t),
    )


def mut(val: float, std: float, lo: float, hi: float, rate: float) -> float:
    if random.random() < rate:
        val = float(np.random.normal(val, std * (hi - lo)))
    return clamp(val, lo, hi)


def mutate_prey(g: PreyGenome, p):
    return PreyGenome(
        speed=mut(g.speed, p.mutation_std, p.speed_min, p.speed_max, p.mutation_rate),
        vision=mut(
            g.vision, p.mutation_std, p.vision_min, p.vision_max, p.mutation_rate
        ),
        stamina=mut(
            g.stamina, p.mutation_std, p.stamina_min, p.stamina_max, p.mutation_rate
        ),
        resistance=mut(
            g.resistance, p.mutation_std, p.resist_min, p.resist_max, p.mutation_rate
        ),
    )


def mutate_pred(g: PredatorGenome, p):
    return PredatorGenome(
        speed=mut(g.speed, p.mutation_std, p.speed_min, p.speed_max, p.mutation_rate),
        vision=mut(
            g.vision, p.mutation_std, p.vision_min, p.vision_max, p.mutation_rate
        ),
        stamina=mut(
            g.stamina, p.mutation_std, p.stamina_min, p.stamina_max, p.mutation_rate
        ),
        strength=mut(
            g.strength, p.mutation_std, p.strength_min, p.strength_max, p.mutation_rate
        ),
    )


def tournament_select(pop, fitness, k: int):
    # pop: list of genomes, fitness: list of floats with same length
    best_i = None
    n = len(pop)
    for _ in range(k):
        i = random.randrange(n)
        if best_i is None or fitness[i] > fitness[best_i]:
            best_i = i
    return pop[best_i]
