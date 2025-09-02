"""
Evolution and genetic algorithm implementation for Darwin simulation.
"""

from typing import List
from ..genetics.dna import PreyGenome, PredatorGenome
from ..genetics.selection import tournament_select
from ..genetics.crossover import crossover_prey, crossover_pred
from ..genetics.mutation import mutate_prey, mutate_pred


class EvolutionEngine:
    """Handles genetic algorithm operations for evolution."""

    @staticmethod
    def evolve_prey_population(
        prey_genomes: List[PreyGenome],
        fitness_scores: List[float],
        target_population: int,
        params,
    ) -> List[PreyGenome]:
        """
        Evolve prey population using genetic algorithms.

        Args:
            prey_genomes: Current generation genomes
            fitness_scores: Corresponding fitness scores
            target_population: Desired population size
            params: Simulation parameters

        Returns:
            New generation of prey genomes
        """
        # Sort by fitness (descending)
        genome_fitness_pairs = list(zip(prey_genomes, fitness_scores))
        genome_fitness_pairs.sort(key=lambda x: x[1], reverse=True)

        sorted_genomes = [pair[0] for pair in genome_fitness_pairs]
        sorted_fitness = [pair[1] for pair in genome_fitness_pairs]

        # Keep top performers
        elite_count = max(1, target_population // 10)  # Keep top 10%
        next_generation = sorted_genomes[:elite_count]

        # Generate rest through genetic operations
        while len(next_generation) < target_population:
            parent1 = tournament_select(
                sorted_genomes, sorted_fitness, params.tournament_k
            )
            parent2 = tournament_select(
                sorted_genomes, sorted_fitness, params.tournament_k
            )

            child = crossover_prey(parent1, parent2, params.crossover_rate)
            child = mutate_prey(child, params)
            next_generation.append(child)

        return next_generation

    @staticmethod
    def evolve_predator_population(
        pred_genomes: List[PredatorGenome],
        fitness_scores: List[float],
        target_population: int,
        params,
    ) -> List[PredatorGenome]:
        """
        Evolve predator population using genetic algorithms.

        Args:
            pred_genomes: Current generation genomes
            fitness_scores: Corresponding fitness scores
            target_population: Desired population size
            params: Simulation parameters

        Returns:
            New generation of predator genomes
        """
        # Sort by fitness (descending)
        genome_fitness_pairs = list(zip(pred_genomes, fitness_scores))
        genome_fitness_pairs.sort(key=lambda x: x[1], reverse=True)

        sorted_genomes = [pair[0] for pair in genome_fitness_pairs]
        sorted_fitness = [pair[1] for pair in genome_fitness_pairs]

        # Keep top performers
        elite_count = max(1, target_population // 10)  # Keep top 10%
        next_generation = sorted_genomes[:elite_count]

        # Generate rest through genetic operations
        while len(next_generation) < target_population:
            parent1 = tournament_select(
                sorted_genomes, sorted_fitness, params.tournament_k
            )
            parent2 = tournament_select(
                sorted_genomes, sorted_fitness, params.tournament_k
            )

            child = crossover_pred(parent1, parent2, params.crossover_rate)
            child = mutate_pred(child, params)
            next_generation.append(child)

        return next_generation
