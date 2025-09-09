
import random
from .genomes import PredatorGenome, PreyGenome

class GeneticOperations:
    
    @staticmethod
    def crossover_predator(parent1: PredatorGenome, parent2: PredatorGenome, 
                          mutation_rate: float = 0.1) -> PredatorGenome:
        # Per-gene crossover: each characteristic has 50% chance from each parent
        child_genome = PredatorGenome(
            speed=parent1.speed if random.random() < 0.5 else parent2.speed,
            vision=parent1.vision if random.random() < 0.5 else parent2.vision,
            stamina=parent1.stamina if random.random() < 0.5 else parent2.stamina,
            attack_strength=parent1.attack_strength if random.random() < 0.5 else parent2.attack_strength
        )
        
        # Apply mutations to each gene individually
        child_genome = GeneticOperations._mutate_predator(child_genome, mutation_rate)
        return child_genome
    
    @staticmethod
    def crossover_prey(parent1: PreyGenome, parent2: PreyGenome, 
                      mutation_rate: float = 0.1) -> PreyGenome:
        # Per-gene crossover: each characteristic has 50% chance from each parent
        child_genome = PreyGenome(
            speed=parent1.speed if random.random() < 0.5 else parent2.speed,
            vision=parent1.vision if random.random() < 0.5 else parent2.vision,
            stamina=parent1.stamina if random.random() < 0.5 else parent2.stamina,
            attack_resistance=parent1.attack_resistance if random.random() < 0.5 else parent2.attack_resistance
        )
        
        # Apply mutations to each gene individually
        child_genome = GeneticOperations._mutate_prey(child_genome, mutation_rate)
        return child_genome
    
    @staticmethod
    def _mutate_predator(genome: PredatorGenome, mutation_rate: float) -> PredatorGenome:
        
        # Try to mutate each gene with the given probability
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
        
        # Try to mutate each gene with the given probability
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
