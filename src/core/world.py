"""
World management and simulation logic for Darwin simulation.
"""

import random
from dataclasses import dataclass, field
from typing import List
from ..entities.prey import Prey
from ..entities.predator import Predator
from ..entities.food import Food
from ..genetics.dna import PreyGenome, PredatorGenome
from ..genetics.generation import random_prey, random_pred
from ..utils.position_utils import rand_pos
from .statistics import Stats, StatisticsCalculator
from .fitness import FitnessCalculator
from .evolution import EvolutionEngine


@dataclass
class World:
    """Main world container that manages all simulation entities and state."""
    params: object
    preys: List[Prey] = field(default_factory=list)
    predators: List[Predator] = field(default_factory=list)
    foods: List[Food] = field(default_factory=list)
    time: int = 0
    generation: int = 0
    history: List[Stats] = field(default_factory=list)
    prey_genomes: List[PreyGenome] = field(default_factory=list)
    pred_genomes: List[PredatorGenome] = field(default_factory=list)
    
    # Helper components
    fitness_calc: FitnessCalculator = field(default_factory=FitnessCalculator)
    stats_calc: StatisticsCalculator = field(default_factory=StatisticsCalculator)
    evolution_engine: EvolutionEngine = field(default_factory=EvolutionEngine)

    def reset_population(self, prey_genomes: List[PreyGenome] = None, pred_genomes: List[PredatorGenome] = None):
        """Reset the world with new populations."""
        W, H = self.params.world_w, self.params.world_h
        
        # Clear current populations
        self.preys = []
        self.predators = []
        self.foods = [Food(rand_pos(W, H)) for _ in range(self.params.food_count)]
        self.time = 0

        # Generate genomes if not provided
        if prey_genomes is None:
            prey_genomes = [random_prey(self.params) for _ in range(self.params.population_prey)]
        if pred_genomes is None:
            pred_genomes = [random_pred(self.params) for _ in range(self.params.population_pred)]

        # Create agents from genomes
        for genome in prey_genomes:
            pos = rand_pos(W, H)
            # Convert stamina (1-100) to actual energy (50-250)
            max_energy = genome.stamina / 100.0 * 200.0 + 50.0
            prey = Prey(x=pos[0], y=pos[1], dna=genome, energy=max_energy)
            self.preys.append(prey)

        for genome in pred_genomes:
            pos = rand_pos(W, H)
            # Convert stamina (1-100) to actual energy (50-250) 
            max_energy = genome.stamina / 100.0 * 200.0 + 50.0
            predator = Predator(x=pos[0], y=pos[1], dna=genome, energy=max_energy)
            self.predators.append(predator)

        # Store genomes for evolution
        self.prey_genomes = prey_genomes.copy()
        self.pred_genomes = pred_genomes.copy()

    def spawn_food_if_needed(self):
        """Spawn new food if population is below threshold."""
        if len(self.foods) < self.params.food_count:
            W, H = self.params.world_w, self.params.world_h
            self.foods.append(Food(rand_pos(W, H)))

    def step(self):
        """Execute one simulation step."""
        self.time += 1
        W, H = self.params.world_w, self.params.world_h

        # Update all agents
        for prey in self.preys:
            if prey.alive:
                prey.step(W, H, self.foods, self.predators, self.preys, self.params)

        for predator in self.predators:
            if predator.alive:
                predator.step(W, H, self.preys, self.predators, self.params)

        # Remove dead agents from simulation
        self.remove_dead_agents()

        # Spawn food as needed
        self.spawn_food_if_needed()

    def remove_dead_agents(self):
        """Remove agents that have died (energy <= 0) from the simulation."""
        # Filter out dead prey
        self.preys = [prey for prey in self.preys if prey.alive]
        
        # Filter out dead predators
        self.predators = [predator for predator in self.predators if predator.alive]

    def spawn_food_if_needed(self):
        """Spawn new food if population is below threshold."""
        if len(self.foods) < self.params.food_count:
            W, H = self.params.world_w, self.params.world_h
            self.foods.append(Food(rand_pos(W, H)))

    def end_generation(self):
        """Process end of generation and calculate statistics."""
        # Calculate reproduction-based fitness (how many agents achieved reproduction score)
        reproducing_prey = [p for p in self.preys if p.alive and p.can_reproduce()]
        reproducing_predators = [p for p in self.predators if p.alive and p.can_reproduce()]
        
        # Calculate fitness scores
        prey_fitness = [self.fitness_calc.prey_fitness(p) for p in self.preys]
        pred_fitness = [self.fitness_calc.pred_fitness(p) for p in self.predators]

        # Calculate average fitness
        prey_fitness_avg = sum(prey_fitness) / len(prey_fitness) if prey_fitness else 0.0
        pred_fitness_avg = sum(pred_fitness) / len(pred_fitness) if pred_fitness else 0.0

        # Calculate average genomes
        prey_source = [p.dna for p in self.preys if p.alive] or self.prey_genomes
        pred_source = [p.dna for p in self.predators if p.alive] or self.pred_genomes
        
        avg_prey_genome = self.stats_calc.calculate_average_prey_genome(prey_source)
        avg_pred_genome = self.stats_calc.calculate_average_pred_genome(pred_source)

        # Create and store statistics (including reproduction success rate)
        stats = Stats(
            generation=self.generation,
            prey_pop=len([p for p in self.preys if p.alive]),
            pred_pop=len([p for p in self.predators if p.alive]),
            prey_fitness_avg=prey_fitness_avg,
            pred_fitness_avg=pred_fitness_avg,
            avg_prey_genome=avg_prey_genome,
            avg_pred_genome=avg_pred_genome
        )
        self.history.append(stats)

        # Evolve populations for next generation using reproduction-ready agents as elite
        # Use agents that achieved reproduction as the "fittest" for next generation
        reproduction_ready_prey = [p.dna for p in reproducing_prey]
        reproduction_ready_pred = [p.dna for p in reproducing_predators]
        
        if reproduction_ready_prey:
            # Reproduce from successful agents
            reproduction_fitness = [p.reproduction_score for p in reproducing_prey]
            self.prey_genomes = self.evolution_engine.evolve_prey_population(
                reproduction_ready_prey, reproduction_fitness, 
                self.params.population_prey, self.params
            )
        elif len([p for p in self.preys if p.alive]) > 0:
            # Fallback to traditional fitness if no reproduction occurred
            surviving_prey_genomes = [p.dna for p in self.preys if p.alive]
            surviving_prey_fitness = [self.fitness_calc.prey_fitness(p) for p in self.preys if p.alive]
            self.prey_genomes = self.evolution_engine.evolve_prey_population(
                surviving_prey_genomes, surviving_prey_fitness, 
                self.params.population_prey, self.params
            )
        
        if reproduction_ready_pred:
            # Reproduce from successful agents
            reproduction_fitness = [p.reproduction_score for p in reproducing_predators]
            self.pred_genomes = self.evolution_engine.evolve_predator_population(
                reproduction_ready_pred, reproduction_fitness,
                self.params.population_pred, self.params
            )
        elif len([p for p in self.predators if p.alive]) > 0:
            # Fallback to traditional fitness if no reproduction occurred
            surviving_pred_genomes = [p.dna for p in self.predators if p.alive]
            surviving_pred_fitness = [self.fitness_calc.pred_fitness(p) for p in self.predators if p.alive] 
            self.pred_genomes = self.evolution_engine.evolve_predator_population(
                surviving_pred_genomes, surviving_pred_fitness,
                self.params.population_pred, self.params
            )

    def new_generation(self):
        """Start a new generation."""
        self.generation += 1
        self.reset_population(self.prey_genomes, self.pred_genomes)
