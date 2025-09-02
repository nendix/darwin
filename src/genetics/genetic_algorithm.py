"""
Darwin - Genetic Algorithm Implementation
"""

import random
from typing import List, Tuple
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


class GeneticAlgorithm:
    """Genetic algorithm operations for evolution"""
    
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
    
    @staticmethod
    def crossover_predator(parent1: PredatorGenome, parent2: PredatorGenome, 
                          mutation_rate: float = 0.1) -> PredatorGenome:
        """Create offspring from two predator parents with crossover and mutation"""
        # Single-point crossover
        if random.random() < 0.5:
            child_genome = PredatorGenome(
                speed=parent1.speed,
                vision=parent1.vision,
                stamina=parent2.stamina,
                attack_strength=parent2.attack_strength
            )
        else:
            child_genome = PredatorGenome(
                speed=parent2.speed,
                vision=parent2.vision,
                stamina=parent1.stamina,
                attack_strength=parent1.attack_strength
            )
        
        # Apply mutations
        child_genome = GeneticAlgorithm._mutate_predator(child_genome, mutation_rate)
        return child_genome
    
    @staticmethod
    def crossover_prey(parent1: PreyGenome, parent2: PreyGenome, 
                      mutation_rate: float = 0.1) -> PreyGenome:
        """Create offspring from two prey parents with crossover and mutation"""
        # Single-point crossover
        if random.random() < 0.5:
            child_genome = PreyGenome(
                speed=parent1.speed,
                vision=parent1.vision,
                stamina=parent2.stamina,
                attack_resistance=parent2.attack_resistance
            )
        else:
            child_genome = PreyGenome(
                speed=parent2.speed,
                vision=parent2.vision,
                stamina=parent1.stamina,
                attack_resistance=parent1.attack_resistance
            )
        
        # Apply mutations
        child_genome = GeneticAlgorithm._mutate_prey(child_genome, mutation_rate)
        return child_genome
    
    @staticmethod
    def _mutate_predator(genome: PredatorGenome, mutation_rate: float) -> PredatorGenome:
        """Apply mutations to predator genome"""
        if random.random() < mutation_rate:
            genome.speed += random.gauss(0, 5)
        if random.random() < mutation_rate:
            genome.vision += random.gauss(0, 5)
        if random.random() < mutation_rate:
            genome.stamina += random.gauss(0, 5)
        if random.random() < mutation_rate:
            genome.attack_strength += random.gauss(0, 5)
        
        # Ensure values stay within bounds
        genome.__post_init__()
        return genome
    
    @staticmethod
    def _mutate_prey(genome: PreyGenome, mutation_rate: float) -> PreyGenome:
        """Apply mutations to prey genome"""
        if random.random() < mutation_rate:
            genome.speed += random.gauss(0, 5)
        if random.random() < mutation_rate:
            genome.vision += random.gauss(0, 5)
        if random.random() < mutation_rate:
            genome.stamina += random.gauss(0, 5)
        if random.random() < mutation_rate:
            genome.attack_resistance += random.gauss(0, 5)
        
        # Ensure values stay within bounds
        genome.__post_init__()
        return genome
