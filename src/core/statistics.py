"""
Statistics tracking and calculation for Darwin simulation.
"""

from dataclasses import dataclass
from typing import List, Optional
from ..genetics.dna import PreyGenome, PredatorGenome


@dataclass
class Stats:
    """Statistics for a single generation."""

    generation: int = 0
    prey_pop: int = 0
    pred_pop: int = 0
    prey_fitness_avg: float = 0.0
    pred_fitness_avg: float = 0.0
    avg_prey_genome: Optional[PreyGenome] = None
    avg_pred_genome: Optional[PredatorGenome] = None


class StatisticsCalculator:
    """Handles calculation of generation statistics."""

    @staticmethod
    def calculate_average_prey_genome(prey_genomes: List[PreyGenome]) -> PreyGenome:
        """Calculate average genome across all prey."""
        if not prey_genomes:
            return PreyGenome(1, 1, 1, 0)

        n = len(prey_genomes)
        avg_speed = sum(g.speed for g in prey_genomes) / n
        avg_vision = sum(g.vision for g in prey_genomes) / n
        avg_stamina = sum(g.stamina for g in prey_genomes) / n
        avg_resistance = sum(g.resistance for g in prey_genomes) / n

        return PreyGenome(
            speed=avg_speed,
            vision=avg_vision,
            stamina=avg_stamina,
            resistance=avg_resistance,
        )

    @staticmethod
    def calculate_average_pred_genome(
        pred_genomes: List[PredatorGenome],
    ) -> PredatorGenome:
        """Calculate average genome across all predators."""
        if not pred_genomes:
            return PredatorGenome(1, 1, 1, 1)

        n = len(pred_genomes)
        avg_speed = sum(g.speed for g in pred_genomes) / n
        avg_vision = sum(g.vision for g in pred_genomes) / n
        avg_stamina = sum(g.stamina for g in pred_genomes) / n
        avg_strength = sum(g.strength for g in pred_genomes) / n

        return PredatorGenome(
            speed=avg_speed,
            vision=avg_vision,
            stamina=avg_stamina,
            strength=avg_strength,
        )
