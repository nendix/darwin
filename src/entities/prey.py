"""
Darwin - Prey Entity Implementation
"""

import math
import random
import pygame
from typing import List, Tuple, Optional

from .base_entity import Entity
from ..config import *
from ..genetics.operations import GeneticOperations
from ..genetics.genomes import PreyGenome, GenomeFactory


class Prey(Entity):
    """Prey entity that avoids predators and seeks food"""

    def __init__(self, x: float, y: float, genome: Optional[PreyGenome] = None):
        if genome is None:
            genome = GenomeFactory.create_random_prey_genome()
        super().__init__(x, y, genome)

    def can_see(self, target: Entity) -> bool:
        """Prey have 360-degree vision"""
        return super().can_see(target)  # Use base distance check only

    def update(self, dt: float, entities: List[Entity]):
        """Update prey behavior"""
        if not self.alive:
            return

        self.update_energy(dt)

        if not self.alive:
            return

        # Check reproduction status
        self.check_reproduction_status()

        # Behavior logic
        if self.can_reproduce:
            self._seek_mate(entities, dt)
        else:
            self._survival_behavior(entities, dt)

        self.move(dt)

        # Check for collisions with same species and resolve
        self.check_collision(entities)

    def _survival_behavior(self, entities: List[Entity], dt: float):
        """Survival behavior - avoid predators and seek food"""
        # Find closest visible predator
        from .predator import Predator  # Import here to avoid circular import

        closest_predator = self.find_closest_visible(entities, Predator)

        if closest_predator:
            # Flee from predator
            flee_angle = self.angle_to(closest_predator) + math.pi  # Opposite direction
            self.direction = flee_angle
        else:
            # Seek food
            from .food import Food  # Import here to avoid circular import

            closest_food = self.find_closest_visible(entities, Food)
            if closest_food:
                self.turn_towards(closest_food, 0.15)

                # Check for eating
                if self.distance_to(closest_food) <= PREY_RADIUS + FOOD_RADIUS:
                    self._eat_food(closest_food, entities)
            else:
                self.random_walk(dt)

    def _seek_mate(self, entities: List[Entity], dt: float):
        """Seek another prey for reproduction"""
        potential_mates = [
            e
            for e in entities
            if isinstance(e, Prey) and e.alive and e.can_reproduce and e != self
        ]

        if potential_mates:
            closest_mate = min(potential_mates, key=self.distance_to)
            self.turn_towards(closest_mate, 0.15)

            # Check for reproduction
            if self.distance_to(closest_mate) <= PREY_RADIUS * 2:
                self._reproduce(closest_mate, entities)
        else:
            self.random_walk(dt)

    def _eat_food(self, food, entities: List[Entity]):
        """Eat food and gain energy"""
        self.energy = min(self.max_energy, self.energy + food.energy_value)
        self.reproduction_score += PREY_EATING_GAIN
        food.alive = False
        entities.remove(food)

    def _reproduce(self, mate, entities: List[Entity]):
        """Reproduce with another prey"""
        # Create offspring
        child_genome = GeneticOperations.crossover_prey(self.genome, mate.genome)
        child = Prey(self.x, self.y, child_genome)
        entities.append(child)

        # Reset reproduction status
        self.reproduction_score = 0
        mate.reproduction_score = 0
        self.can_reproduce = False
        mate.can_reproduce = False

    def take_damage(self, damage: float):
        """Take damage from predator attack"""
        self.damage_taken += damage
        if self.damage_taken >= self.genome.attack_resistance:
            self.alive = False

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset: Tuple[int, int],
        show_vision: bool = False,
    ):
        """Draw prey as blue circle with optional vision range"""
        screen_x, screen_y = self.get_screen_position(camera_offset)

        if (
            -50 <= screen_x <= SCREEN_WIDTH + 50
            and -50 <= screen_y <= SCREEN_HEIGHT + 50
        ):
            # Draw vision range if enabled (simple circle outline)
            if show_vision:
                vision_range = self.get_vision_range()
                pygame.draw.circle(
                    screen, BLUE, (screen_x, screen_y), int(vision_range), 2
                )

            # Draw prey
            color = BLUE if not self.can_reproduce else YELLOW
            pygame.draw.circle(screen, color, (screen_x, screen_y), PREY_RADIUS)
