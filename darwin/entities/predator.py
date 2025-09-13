import math
import random
import pygame
from typing import List, Optional

from .base_entity import Entity
from ..genetics.genomes import PredatorGenome
from ..genetics.genomes import GenomeFactory
from ..genetics.operations import GeneticOperations
from darwin import config as c


class Predator(Entity):
    def __init__(self, x: float, y: float, genome: Optional[PredatorGenome] = None):
        if genome is None:
            genome = GenomeFactory.create_random_predator_genome()
        super().__init__(x, y, genome)
        self.target_prey = None

    def can_see(self, target: Entity) -> bool:
        # First check distance
        if not super().can_see(target):
            return False

        # Then check if in vision cone
        return self._is_in_vision_cone(target)

    def _is_in_vision_cone(self, target: Entity) -> bool:
        angle_to_target = self.angle_to(target)
        angle_diff = abs(angle_to_target - self.direction)

        # Normalize angle difference
        while angle_diff > math.pi:
            angle_diff = abs(angle_diff - 2 * math.pi)

        half_cone_angle = math.radians(c.PREDATOR_VISION_ANGLE / 2)
        return angle_diff <= half_cone_angle

    def update(self, dt: float, entities: List[Entity]):
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
            self._hunt_behavior(entities, dt)

        self.move(dt)

        # Check for collisions with same species and resolve
        self.check_collision(entities)

    def _hunt_behavior(self, entities: List[Entity], dt: float):
        # Find closest visible prey
        from .prey import Prey  # Import here to avoid circular import

        closest_prey = self.find_closest_visible(entities, Prey)

        if closest_prey:
            self.target_prey = closest_prey
            self.turn_towards(closest_prey, 0.2)

            # Check for attack
            if self.distance_to(closest_prey) <= c.ENTITY_RADIUS + c.ENTITY_RADIUS:
                self._attack_prey(closest_prey)
        else:
            self.target_prey = None
            self.random_walk(dt)

    def _seek_mate(self, entities: List[Entity], dt: float):
        potential_mates = [
            e
            for e in entities
            if isinstance(e, Predator) and e.alive and e.can_reproduce and e != self
        ]

        if potential_mates:
            closest_mate = min(potential_mates, key=self.distance_to)
            self.turn_towards(closest_mate, 0.15)

            # Check for reproduction
            if self.distance_to(closest_mate) <= c.ENTITY_RADIUS * 2:
                self._reproduce(closest_mate, entities)
        else:
            self.random_walk(dt)

    def _attack_prey(self, prey):
        from .prey import Prey

        if isinstance(prey, Prey):
            was_alive = prey.alive
            prey.take_damage(self.genome.attack_strength)

            # Only get reproduction points if the prey dies from this attack
            if was_alive and not prey.alive:
                self.reproduction_score += c.PREDATOR_EATING_GAIN

    def _reproduce(self, mate, entities: List[Entity]):
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

    def draw(
        self,
        screen: pygame.Surface,
        show_vision: bool = False,
    ):
        screen_x, screen_y = int(self.x), int(self.y)

        if (
            -50 <= screen_x <= c.SCREEN_WIDTH + 50
            and -50 <= screen_y <= c.SCREEN_HEIGHT + 50
        ):
            # Draw vision cone if enabled
            if show_vision:
                self._draw_vision_cone(screen, screen_x, screen_y)

            # Draw predator
            color = c.RED if not self.can_reproduce else c.YELLOW
            pygame.draw.circle(screen, color, (screen_x, screen_y), c.ENTITY_RADIUS)

    def _draw_vision_cone(self, screen: pygame.Surface, screen_x: int, screen_y: int):
        vision_range = self.genome.vision
        half_cone_angle = math.radians(c.PREDATOR_VISION_ANGLE / 2)

        # Calculate cone edges
        left_angle = self.direction - half_cone_angle
        right_angle = self.direction + half_cone_angle

        # Draw vision lines
        left_end_x = screen_x + math.cos(left_angle) * vision_range
        left_end_y = screen_y + math.sin(left_angle) * vision_range
        right_end_x = screen_x + math.cos(right_angle) * vision_range
        right_end_y = screen_y + math.sin(right_angle) * vision_range

        # Draw the cone outline with simple lines
        pygame.draw.line(
            screen, c.RED, (screen_x, screen_y), (left_end_x, left_end_y), 2
        )
        pygame.draw.line(
            screen, c.RED, (screen_x, screen_y), (right_end_x, right_end_y), 2
        )
        pygame.draw.line(
            screen, c.RED, (left_end_x, left_end_y), (right_end_x, right_end_y), 2
        )
