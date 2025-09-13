import random
from dataclasses import dataclass

from darwin import config as c


@dataclass
class Genome:
    speed: float
    vision: float
    stamina: float

    def __post_init__(self):
        self.speed = max(c.MIN_GENE, min(c.MAX_GENE, self.speed))
        self.vision = max(c.MIN_GENE, min(c.MAX_GENE, self.vision))
        self.stamina = max(c.MIN_GENE, min(c.MAX_GENE, self.stamina))


@dataclass
class PredatorGenome(Genome):
    attack_strength: float

    def __post_init__(self):
        super().__post_init__()
        self.attack_strength = max(c.MIN_GENE, min(c.MAX_GENE, self.attack_strength))


@dataclass
class PreyGenome(Genome):
    attack_resistance: float

    def __post_init__(self):
        super().__post_init__()
        self.attack_resistance = max(
            c.MIN_GENE, min(c.MAX_GENE, self.attack_resistance)
        )


class GenomeFactory:

    @staticmethod
    def create_random_predator_genome() -> PredatorGenome:
        return PredatorGenome(
            speed=random.uniform(c.MIN_GENE, c.MAX_GENE),
            vision=random.uniform(c.MIN_GENE, c.MAX_GENE),
            stamina=random.uniform(c.MIN_GENE, c.MAX_GENE),
            attack_strength=random.uniform(c.MIN_GENE, c.MAX_GENE),
        )

    @staticmethod
    def create_random_prey_genome() -> PreyGenome:
        return PreyGenome(
            speed=random.uniform(c.MIN_GENE, c.MAX_GENE),
            vision=random.uniform(c.MIN_GENE, c.MAX_GENE),
            stamina=random.uniform(c.MIN_GENE, c.MAX_GENE),
            attack_resistance=random.uniform(c.MIN_GENE, c.MAX_GENE),
        )
