"""
Darwin - Genome Definitions and Factory
"""

import random
from dataclasses import dataclass


@dataclass
class Genome:
    """Base genome class"""
    speed: float
    vision: float
    stamina: float
    
    def __post_init__(self):
        """Ensure gene values are within valid range"""
        self.speed = max(1, min(100, self.speed))
        self.vision = max(1, min(100, self.vision))
        self.stamina = max(1, min(100, self.stamina))


@dataclass
class PredatorGenome(Genome):
    """Predator-specific genome with attack strength"""
    attack_strength: float
    
    def __post_init__(self):
        super().__post_init__()
        self.attack_strength = max(1, min(100, self.attack_strength))


@dataclass
class PreyGenome(Genome):
    """Prey-specific genome with attack resistance"""
    attack_resistance: float
    
    def __post_init__(self):
        super().__post_init__()
        self.attack_resistance = max(1, min(100, self.attack_resistance))


class GenomeFactory:
    """Factory for creating random genomes"""
    
    @staticmethod
    def create_random_predator_genome() -> PredatorGenome:
        """Create a random predator genome"""
        return PredatorGenome(
            speed=random.uniform(1, 100),
            vision=random.uniform(1, 100),
            stamina=random.uniform(1, 100),
            attack_strength=random.uniform(1, 100)
        )
    
    @staticmethod
    def create_random_prey_genome() -> PreyGenome:
        """Create a random prey genome"""
        return PreyGenome(
            speed=random.uniform(1, 100),
            vision=random.uniform(1, 100),
            stamina=random.uniform(1, 100),
            attack_resistance=random.uniform(1, 100)
        )
