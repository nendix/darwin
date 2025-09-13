import random
import time
from typing import List, Dict, Any, Tuple

from ..entities import Predator, Prey, Food, Entity
from ..genetics.operations import GeneticOperations
from darwin import config as c


class Simulation:

    def __init__(self, params: Dict[str, Any]):
        self.params = params
        self.entities: List[Entity] = []
        self.time_remaining = params["duration"]
        self.speed = params["speed"]
        self.show_vision = params["show_vision"]
        self.start_time = time.time()

        self.total_reproductions = 0
        self.total_mutations = 0
        self.population_history = {"predators": [], "prey": [], "time": []}

        # Add simulation stats reference to entities for tracking
        self.simulation_stats = {"total_reproductions": 0, "total_mutations": 0}

        # Initialize populations
        self._initialize_populations()
        self._spawn_food()

        # Record initial population
        self._record_population_data()

    def _initialize_populations(self):
        # Create predators
        for _ in range(self.params["predator_count"]):
            x = random.uniform(50, c.SCREEN_WIDTH - 50)
            y = random.uniform(50, c.SCREEN_HEIGHT - 50)
            predator = Predator(x, y)
            self.entities.append(predator)

        # Create prey
        for _ in range(self.params["prey_count"]):
            x = random.uniform(50, c.SCREEN_WIDTH - 50)
            y = random.uniform(50, c.SCREEN_HEIGHT - 50)
            prey = Prey(x, y)
            self.entities.append(prey)

    def _spawn_food(self):
        current_food = len(
            [e for e in self.entities if isinstance(e, Food) and e.available]
        )
        food_needed = self.params["food_count"] - current_food

        for _ in range(food_needed):
            x = random.uniform(20, c.SCREEN_WIDTH - 20)
            y = random.uniform(20, c.SCREEN_HEIGHT - 20)
            food = Food(x, y)
            self.entities.append(food)

    def _record_population_data(self):
        predator_count = len(
            [e for e in self.entities if isinstance(e, Predator) and e.alive]
        )
        prey_count = len([e for e in self.entities if isinstance(e, Prey) and e.alive])

        self.population_history["predators"].append(predator_count)
        self.population_history["prey"].append(prey_count)
        self.population_history["time"].append(
            self.params["duration"] - self.time_remaining
        )

    def update(self, dt: float):
        # Adjust dt by simulation speed
        dt *= self.speed

        # Update timer
        self.time_remaining -= dt

        # Count entities before update
        initial_count = len(self.entities)

        # Update all entities
        for entity in self.entities[
            :
        ]:  # Use slice to avoid modification during iteration
            if isinstance(entity, Food):
                if entity.available:
                    entity.update(dt, self.entities)
            else:
                if entity.alive:
                    entity.update(dt, self.entities)

        # Count reproductions based on entity count increase
        final_count = len(self.entities)
        if final_count > initial_count:
            new_births = final_count - initial_count
            self.total_reproductions += new_births

        # Remove dead entities
        self.entities = [
            e
            for e in self.entities
            if (isinstance(e, Food) and e.available)
            or (not isinstance(e, Food) and e.alive)
        ]

        # Maintain food supply
        self._spawn_food()

        # Record population data periodically
        if int(self.time_remaining) % 5 == 0:  # Every 5 seconds
            self._record_population_data()

    def increase_speed(self):
        self.speed = min(c.MAX_SIMULATION_SPEED, self.speed + 1)

    def decrease_speed(self):
        self.speed = max(c.MIN_SIMULATION_SPEED, self.speed - 1)

    def is_finished(self) -> bool:
        return self.time_remaining <= 0

    def draw(self, screen, show_vision: bool):
        # Sort entities by type for proper layering (food, prey, predators)
        food_entities = [e for e in self.entities if isinstance(e, Food)]
        prey_entities = [e for e in self.entities if isinstance(e, Prey)]
        predator_entities = [e for e in self.entities if isinstance(e, Predator)]

        # Draw in order: food, prey, predators
        for entity in food_entities:
            entity.draw(screen)
        for entity in prey_entities + predator_entities:
            entity.draw(screen, show_vision)

    def get_statistics(self) -> Dict[str, Any]:
        predator_count = len(
            [e for e in self.entities if isinstance(e, Predator) and e.alive]
        )
        prey_count = len([e for e in self.entities if isinstance(e, Prey) and e.alive])

        # Calculate survival rates
        initial_predators = self.params["predator_count"]
        initial_prey = self.params["prey_count"]

        predator_survival_rate = (
            (predator_count / initial_predators) * 100 if initial_predators > 0 else 0
        )
        prey_survival_rate = (
            (prey_count / initial_prey) * 100 if initial_prey > 0 else 0
        )

        # Get average genome stats
        predator_stats = self._calculate_genome_statistics("predator")
        prey_stats = self._calculate_genome_statistics("prey")

        return {
            "final_populations": {"predators": predator_count, "prey": prey_count},
            "survival_stats": {
                "predator_survival_rate": predator_survival_rate,
                "prey_survival_rate": prey_survival_rate,
            },
            "evolution_info": {
                "total_reproductions": self.total_reproductions,
                "total_mutations": self.total_mutations,
            },
            "genome_statistics": {"predators": predator_stats, "prey": prey_stats},
            "population_history": self.population_history,
            "simulation_params": self.params,
        }

    def _calculate_genome_statistics(self, species: str) -> Dict[str, float]:
        if species == "predator":
            entities = [e for e in self.entities if isinstance(e, Predator) and e.alive]
            if not entities:
                return {"speed": 0, "vision": 0, "stamina": 0, "attack_strength": 0}

            avg_speed = sum(e.genome.speed for e in entities) / len(entities)
            avg_vision = sum(e.genome.vision for e in entities) / len(entities)
            avg_stamina = sum(e.genome.stamina for e in entities) / len(entities)
            avg_attack = sum(e.genome.attack_strength for e in entities) / len(entities)

            return {
                "speed": avg_speed,
                "vision": avg_vision,
                "stamina": avg_stamina,
                "attack_strength": avg_attack,
            }

        elif species == "prey":
            entities = [e for e in self.entities if isinstance(e, Prey) and e.alive]
            if not entities:
                return {"speed": 0, "vision": 0, "stamina": 0, "attack_resistance": 0}

            avg_speed = sum(e.genome.speed for e in entities) / len(entities)
            avg_vision = sum(e.genome.vision for e in entities) / len(entities)
            avg_stamina = sum(e.genome.stamina for e in entities) / len(entities)
            avg_resistance = sum(e.genome.attack_resistance for e in entities) / len(
                entities
            )

            return {
                "speed": avg_speed,
                "vision": avg_vision,
                "stamina": avg_stamina,
                "attack_resistance": avg_resistance,
            }

        return {}


class PopulationManager:

    @staticmethod
    def check_reproduction_opportunities(
        entities: List[Entity],
    ) -> List[Tuple[Entity, Entity]]:
        reproduction_pairs = []

        # Check predator reproduction
        predators = [e for e in entities if isinstance(e, Predator) and e.can_reproduce]
        for i, predator1 in enumerate(predators):
            for predator2 in predators[i + 1 :]:
                if predator1.distance_to(predator2) <= c.ENTITY_RADIUS * 10:
                    reproduction_pairs.append((predator1, predator2))

        # Check prey reproduction
        prey = [e for e in entities if isinstance(e, Prey) and e.can_reproduce]
        for i, prey1 in enumerate(prey):
            for prey2 in prey[i + 1 :]:
                if prey1.distance_to(prey2) <= c.ENTITY_RADIUS * 10:
                    reproduction_pairs.append((prey1, prey2))

        return reproduction_pairs

    @staticmethod
    def handle_reproduction(
        parent1: Entity, parent2: Entity, entities: List[Entity]
    ) -> bool:
        if isinstance(parent1, Predator) and isinstance(parent2, Predator):
            # Create predator offspring
            child_genome = GeneticOperations.crossover_predator(
                parent1.genome, parent2.genome
            )
            child_x = (parent1.x + parent2.x) / 2 + random.uniform(-30, 30)
            child_y = (parent1.y + parent2.y) / 2 + random.uniform(-30, 30)

            # Keep within bounds
            child_x = max(20, min(c.SCREEN_WIDTH - 20, child_x))
            child_y = max(20, min(c.SCREEN_HEIGHT - 20, child_y))

            child = Predator(child_x, child_y, child_genome)
            entities.append(child)

            # Reset parent reproduction status
            parent1.reproduction_score = 0
            parent2.reproduction_score = 0
            parent1.can_reproduce = False
            parent2.can_reproduce = False

            return True

        elif isinstance(parent1, Prey) and isinstance(parent2, Prey):
            # Create prey offspring
            child_genome = GeneticOperations.crossover_prey(
                parent1.genome, parent2.genome
            )
            child_x = (parent1.x + parent2.x) / 2 + random.uniform(-30, 30)
            child_y = (parent1.y + parent2.y) / 2 + random.uniform(-30, 30)

            # Keep within bounds
            child_x = max(20, min(c.SCREEN_WIDTH - 20, child_x))
            child_y = max(20, min(c.SCREEN_HEIGHT - 20, child_y))

            child = Prey(child_x, child_y, child_genome)
            entities.append(child)

            # Reset parent reproduction status
            parent1.reproduction_score = 0
            parent2.reproduction_score = 0
            parent1.can_reproduce = False
            parent2.can_reproduce = False

            return True

        return False
