"""
Fitness calculation functions for Darwin simulation.
"""

from ..entities.prey import Prey
from ..entities.predator import Predator


class FitnessCalculator:
    """Handles fitness calculation for different agent types."""
    
    @staticmethod
    def prey_fitness(prey: Prey) -> float:
        """
        Calculate fitness for a prey agent.
        
        Components:
        - Survival (age): Rewards longevity
        - Food eaten: Rewards successful foraging
        - Energy ratio: Rewards energy management
        """
        age_factor = prey.age * 0.2
        food_factor = prey.food_eaten * 10.0
        energy_factor = (prey.energy / max(1.0, prey.dna.stamina)) * 5.0
        
        return age_factor + food_factor + energy_factor
    
    @staticmethod
    def pred_fitness(predator: Predator) -> float:
        """
        Calculate fitness for a predator agent.
        
        Components:
        - Kills: Rewards successful hunting
        - Survival (age): Rewards longevity
        - Energy ratio: Rewards energy management
        """
        kill_factor = predator.kills * 15.0
        age_factor = predator.age * 0.1
        energy_factor = (predator.energy / max(1.0, predator.dna.stamina)) * 5.0
        
        return kill_factor + age_factor + energy_factor
