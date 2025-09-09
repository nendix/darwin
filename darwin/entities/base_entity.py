"""
Darwin - Base Entity Class for Genetic Entities
"""

import math
import random
import pygame
from typing import List, Tuple, Optional

from darwin import config as c


class Entity:
    """Base class for genetic entities (predators and prey) in the simulation"""

    def __init__(self, x: float, y: float, genome):
        self.x = x
        self.y = y
        self.alive = True

        # Genetic properties
        self.genome = genome
        self.energy = genome.stamina
        self.max_energy = genome.stamina
        self.reproduction_score = 0
        self.damage_taken = 0
        self.direction = random.uniform(0, 2 * math.pi)
        self.can_reproduce = False

    def update(self, dt: float, entities: List["Entity"]):
        """Update entity state - to be implemented by subclasses"""
        pass

    def draw(
        self,
        screen: pygame.Surface,
        camera_offset: Tuple[int, int],
        show_vision: bool = False,
    ):
        """Draw entity on screen - to be implemented by subclasses"""
        pass

    def distance_to(self, other) -> float:
        """Calculate distance to another entity (works with any object with x,y)"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def angle_to(self, other) -> float:
        """Calculate angle to another entity in radians"""
        return math.atan2(other.y - self.y, other.x - self.x)

    def move_in_direction(self, direction: float, speed: float, dt: float):
        """Move entity in a specific direction with given speed"""
        distance = speed * dt
        new_x = self.x + math.cos(direction) * distance
        new_y = self.y + math.sin(direction) * distance

        # Keep within screen bounds
        self.x = max(10, min(c.SCREEN_WIDTH - 10, new_x))
        self.y = max(10, min(c.SCREEN_HEIGHT - 10, new_y))

    def check_collision(self, entities):
        """Check for collision with entities of the same species and resolve"""
        entity_radius = 6  # Both predators and prey have radius 6
        collision_distance = entity_radius * 2  # Minimum distance between centers

        for other in entities:
            if (
                other != self
                and other.alive
                and type(other) == type(self)  # Same species
                and self.distance_to(other) < collision_distance
            ):

                # Calculate separation vector
                dx = self.x - other.x
                dy = self.y - other.y

                # Avoid division by zero
                if dx == 0 and dy == 0:
                    dx = random.uniform(-1, 1)
                    dy = random.uniform(-1, 1)

                # Normalize and apply separation
                distance = math.sqrt(dx * dx + dy * dy)
                if distance > 0:
                    # Move away from other entity
                    separation_strength = (collision_distance - distance) / 2
                    self.x += (dx / distance) * separation_strength
                    self.y += (dy / distance) * separation_strength

                    # Keep within bounds after separation
                    self.x = max(
                        entity_radius, min(c.SCREEN_WIDTH - entity_radius, self.x)
                    )
                    self.y = max(
                        entity_radius, min(c.SCREEN_HEIGHT - entity_radius, self.y)
                    )

    def move(self, dt: float):
        """Move based on genome speed"""
        speed_factor = self.genome.speed / 100.0
        base_speed = 50  # Base speed of 50 pixels per second
        actual_speed = speed_factor * base_speed

        self.move_in_direction(self.direction, actual_speed, dt)

        # Consume energy for movement
        self.energy -= c.MOVEMENT_ENERGY_COST * dt

    def update_energy(self, dt: float):
        """Update energy levels and check for death"""
        self.energy -= c.ENERGY_DECAY_RATE * dt
        self.energy = max(0, min(self.max_energy, self.energy))

        if self.energy <= 0:
            self.alive = False

    def turn_towards(self, target, turn_speed: float = 0.1):
        """Turn towards a target entity"""
        target_angle = self.angle_to(target)
        angle_diff = target_angle - self.direction

        # Normalize angle difference to [-π, π]
        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        # Apply turn speed
        self.direction += angle_diff * turn_speed

    def random_walk(
        self, dt: float, turn_probability: float = 0.1, max_turn: float = 1.0
    ):
        """Perform random walk movement"""
        if random.random() < turn_probability:
            self.direction += random.uniform(-max_turn, max_turn)

    def find_closest_visible(
        self, entities: List, entity_type: type
    ) -> Optional["Entity"]:
        """Find the closest visible entity of a specific type"""
        visible_entities = [
            e
            for e in entities
            if isinstance(e, entity_type) and e.alive and self.can_see(e)
        ]

        if not visible_entities:
            return None

        return min(visible_entities, key=self.distance_to)

    def can_see(self, target) -> bool:
        """Check if entity can see target - basic distance check"""
        distance = self.distance_to(target)
        vision_range = self.get_vision_range()
        return distance <= vision_range

    def check_reproduction_status(self):
        """Check if entity can reproduce"""
        if self.reproduction_score >= c.REPRODUCTION_SCORE_THRESHOLD:
            self.can_reproduce = True
        else:
            self.can_reproduce = False

    def get_vision_range(self) -> float:
        """Get vision range based on genome"""
        return (self.genome.vision / 100.0) * 150  # Max vision range of 150 pixels

    def get_screen_position(self, camera_offset: Tuple[int, int]) -> Tuple[int, int]:
        """Get screen position accounting for camera offset"""
        return (int(self.x - camera_offset[0]), int(self.y - camera_offset[1]))
