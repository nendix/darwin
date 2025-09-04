"""
Darwin - Predator Entity
"""

import math
import random
import pygame
from typing import List, Tuple, Optional

from .base_entity import Entity
from ..genetics.genomes import PredatorGenome
from ..genetics.genomes import GenomeFactory
from ..genetics.operations import GeneticOperations
from ..config import *


class Predator(Entity):
    """Predator entity that hunts prey"""

    def __init__(self, x: float, y: float, genome: Optional[PredatorGenome] = None):
        super().__init__(x, y)
        if genome is None:
            genome = GenomeFactory.create_random_predator_genome()
        self.genome = genome
        self.energy = genome.stamina
        self.max_energy = genome.stamina
        self.reproduction_score = 0
        self.damage_taken = 0
        self.direction = random.uniform(0, 2 * math.pi)
        self.can_reproduce = False
        self.seeking_mate = False
        self.target_prey = None

    def move(self, dt: float):
        """Move the predator based on its speed and direction"""
        speed_factor = self.genome.speed / 100.0
        distance = speed_factor * 50 * dt  # Base speed of 50 pixels per second

        new_x = self.x + math.cos(self.direction) * distance
        new_y = self.y + math.sin(self.direction) * distance

        # Keep within screen bounds (world = screen)
        self.x = max(10, min(SCREEN_WIDTH - 10, new_x))
        self.y = max(10, min(SCREEN_HEIGHT - 10, new_y))

        # Consume energy for movement
        self.energy -= MOVEMENT_ENERGY_COST * dt

    def update_energy(self, dt: float):
        """Update energy levels"""
        self.energy -= ENERGY_DECAY_RATE * dt
        self.energy = max(0, min(self.max_energy, self.energy))

        if self.energy <= 0:
            self.alive = False

    def can_see(self, target: Entity) -> bool:
        """Check if the predator can see a target entity"""
        distance = self.distance_to(target)
        vision_range = (
            self.genome.vision / 100.0
        ) * 150  # Max vision range of 150 pixels

        if distance > vision_range:
            return False

        return self._is_in_vision_cone(target)

    def _is_in_vision_cone(self, target: Entity) -> bool:
        """Predators have cone vision in front of them"""
        angle_to_target = self.angle_to(target)
        angle_diff = abs(angle_to_target - self.direction)

        # Normalize angle difference
        while angle_diff > math.pi:
            angle_diff = abs(angle_diff - 2 * math.pi)

        half_cone_angle = math.radians(PREDATOR_VISION_ANGLE / 2)
        return angle_diff <= half_cone_angle

    def find_closest_visible(
        self, entities: List[Entity], entity_type: type
    ) -> Optional[Entity]:
        """Find the closest visible entity of a specific type"""
        visible_entities = [
            e
            for e in entities
            if isinstance(e, entity_type) and e.alive and self.can_see(e)
        ]

        if not visible_entities:
            return None

        return min(visible_entities, key=self.distance_to)

    def turn_towards(self, target: Entity, turn_speed: float = 0.1):
        """Turn towards a target entity"""
        target_angle = self.angle_to(target)
        angle_diff = target_angle - self.direction

        # Normalize angle difference to [-pi, pi]
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Turn towards target with limited turn speed
        self.direction += max(-turn_speed, min(turn_speed, angle_diff))

    def random_walk(self, dt: float):
        """Perform random movement"""
        if random.random() < 0.1:  # 10% chance to change direction
            self.direction += random.uniform(-0.5, 0.5)

    def update(self, dt: float, entities: List[Entity]):
        """Update predator behavior"""
        if not self.alive:
            return

        self.update_energy(dt)

        if not self.alive:
            return

        # Check reproduction status
        if self.reproduction_score >= REPRODUCTION_SCORE_THRESHOLD:
            self.can_reproduce = True
            self.seeking_mate = True

        # Behavior logic
        if self.seeking_mate:
            self._seek_mate(entities, dt)
        else:
            self._hunt_behavior(entities, dt)

        self.move(dt)

    def _hunt_behavior(self, entities: List[Entity], dt: float):
        """Hunting behavior - find and chase prey"""
        # Find closest visible prey
        from .prey import Prey  # Import here to avoid circular import

        closest_prey = self.find_closest_visible(entities, Prey)

        if closest_prey:
            self.target_prey = closest_prey
            self.turn_towards(closest_prey, 0.2)

            # Check for attack
            if self.distance_to(closest_prey) <= PREDATOR_RADIUS + PREY_RADIUS:
                self._attack_prey(closest_prey)
        else:
            self.target_prey = None
            self.random_walk(dt)

    def _seek_mate(self, entities: List[Entity], dt: float):
        """Seek another predator for reproduction"""
        potential_mates = [
            e
            for e in entities
            if isinstance(e, Predator) and e.alive and e.can_reproduce and e != self
        ]

        if potential_mates:
            closest_mate = min(potential_mates, key=self.distance_to)
            self.turn_towards(closest_mate, 0.15)

            # Check for reproduction
            if self.distance_to(closest_mate) <= PREDATOR_RADIUS * 2:
                self._reproduce(closest_mate, entities)
        else:
            self.random_walk(dt)

    def _attack_prey(self, prey):
        """Attack a prey entity"""
        from .prey import Prey  # Import here to avoid circular import

        if isinstance(prey, Prey):
            prey.take_damage(self.genome.attack_strength)
            self.reproduction_score += PREDATOR_EATING_GAIN

    def _reproduce(self, mate, entities: List[Entity]):
        """Reproduce with another predator"""
        # Create offspring
        child_genome = GeneticOperations.crossover_predator(self.genome, mate.genome)
        child_x = (self.x + mate.x) / 2 + random.uniform(-20, 20)
        child_y = (self.y + mate.y) / 2 + random.uniform(-20, 20)
        child = Predator(child_x, child_y, child_genome)
        entities.append(child)

        # Reset reproduction status
        self.reproduction_score = 0
        mate.reproduction_score = 0
        self.can_reproduce = False
        mate.can_reproduce = False
        self.seeking_mate = False
        mate.seeking_mate = False

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset: Tuple[int, int],
        show_vision: bool = False,
    ):
        """Draw predator as red circle with optional vision cone"""
        screen_x = int(self.x)
        screen_y = int(self.y)

        if (
            -50 <= screen_x <= SCREEN_WIDTH + 50
            and -50 <= screen_y <= SCREEN_HEIGHT + 50
        ):
            # Draw vision cone if enabled
            if show_vision:
                self._draw_vision_cone(screen, screen_x, screen_y)

            # Draw predator
            color = RED if not self.can_reproduce else YELLOW
            pygame.draw.circle(screen, color, (screen_x, screen_y), PREDATOR_RADIUS)

            # Draw direction indicator
            end_x = screen_x + math.cos(self.direction) * PREDATOR_RADIUS
            end_y = screen_y + math.sin(self.direction) * PREDATOR_RADIUS
            pygame.draw.line(screen, WHITE, (screen_x, screen_y), (end_x, end_y), 2)

    def _draw_vision_cone(self, screen: pygame.Surface, screen_x: int, screen_y: int):
        """Draw the predator's vision cone as simple lines"""
        vision_range = (self.genome.vision / 100.0) * 150
        half_cone_angle = math.radians(PREDATOR_VISION_ANGLE / 2)

        # Calculate cone edges
        left_angle = self.direction - half_cone_angle
        right_angle = self.direction + half_cone_angle

        # Draw vision lines
        left_end_x = screen_x + math.cos(left_angle) * vision_range
        left_end_y = screen_y + math.sin(left_angle) * vision_range
        right_end_x = screen_x + math.cos(right_angle) * vision_range
        right_end_y = screen_y + math.sin(right_angle) * vision_range

        # Draw the cone outline with simple lines
        pygame.draw.line(screen, RED, (screen_x, screen_y), (left_end_x, left_end_y), 2)
        pygame.draw.line(
            screen, RED, (screen_x, screen_y), (right_end_x, right_end_y), 2
        )
        pygame.draw.line(
            screen, RED, (left_end_x, left_end_y), (right_end_x, right_end_y), 1
        )
