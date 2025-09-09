import math
import random
import pygame
from typing import List, Optional

from darwin import config as c

class Entity:

    def __init__(self, x: float, y: float, genome):
        self.x = x
        self.y = y
        self.alive = True

        self.genome = genome
        self.energy = genome.stamina
        self.max_energy = genome.stamina
        self.reproduction_score = 0
        self.damage_taken = 0
        self.direction = random.uniform(0, 2 * math.pi)
        self.can_reproduce = False

    def update(self, dt: float, entities: List["Entity"]):
        pass

    def draw(
        self,
        screen: pygame.Surface,
        show_vision: bool = False,
    ):
        pass

    def distance_to(self, other) -> float:
        dx = abs(self.x - other.x)
        dy = abs(self.y - other.y)

        dx = min(dx, c.SCREEN_WIDTH - dx)
        dy = min(dy, c.SCREEN_HEIGHT - dy)

        return math.sqrt(dx * dx + dy * dy)

    def angle_to(self, other) -> float:
        dx = other.x - self.x
        dy = other.y - self.y

        if abs(dx) > c.SCREEN_WIDTH / 2:
            dx = dx - math.copysign(c.SCREEN_WIDTH, dx)
        if abs(dy) > c.SCREEN_HEIGHT / 2:
            dy = dy - math.copysign(c.SCREEN_HEIGHT, dy)

        return math.atan2(dy, dx)

    def move_in_direction(self, direction: float, speed: float, dt: float):
        distance = speed * dt
        new_x = self.x + math.cos(direction) * distance
        new_y = self.y + math.sin(direction) * distance

        self.x = new_x % c.SCREEN_WIDTH
        self.y = new_y % c.SCREEN_HEIGHT

    def check_collision(self, entities):
        entity_radius = 6
        collision_distance = entity_radius * 2

        for other in entities:
            other_alive = (hasattr(other, 'available') and other.available) or (hasattr(other, 'alive') and other.alive)
            
            if (
                other != self
                and other_alive
                and type(other) == type(self)
                and self.distance_to(other) < collision_distance
            ):

                dx = self.x - other.x
                dy = self.y - other.y

                if abs(dx) > c.SCREEN_WIDTH / 2:
                    dx = dx - math.copysign(c.SCREEN_WIDTH, dx)
                if abs(dy) > c.SCREEN_HEIGHT / 2:
                    dy = dy - math.copysign(c.SCREEN_HEIGHT, dy)

                if dx == 0 and dy == 0:
                    dx = random.uniform(-1, 1)
                    dy = random.uniform(-1, 1)

                distance = math.sqrt(dx * dx + dy * dy)
                if distance > 0:
                    separation_strength = (collision_distance - distance) / 2
                    self.x += (dx / distance) * separation_strength
                    self.y += (dy / distance) * separation_strength

                    self.x = self.x % c.SCREEN_WIDTH
                    self.y = self.y % c.SCREEN_HEIGHT

    def move(self, dt: float):
        speed_factor = self.genome.speed / 100.0
        base_speed = 50
        actual_speed = speed_factor * base_speed

        self.move_in_direction(self.direction, actual_speed, dt)

        self.energy -= c.MOVEMENT_ENERGY_COST * dt

    def update_energy(self, dt: float):
        self.energy -= c.ENERGY_DECAY_RATE * dt
        self.energy = max(0, min(self.max_energy, self.energy))

        if self.energy <= 0:
            self.alive = False

    def turn_towards(self, target, turn_speed: float = 0.1):
        target_angle = self.angle_to(target)
        angle_diff = target_angle - self.direction

        while angle_diff > math.pi:
            angle_diff -= 2 * math.pi
        while angle_diff < -math.pi:
            angle_diff += 2 * math.pi

        self.direction += angle_diff * turn_speed

    def random_walk(
        self, dt: float, turn_probability: float = 0.1, max_turn: float = 1.0
    ):
        if random.random() < turn_probability:
            self.direction += random.uniform(-max_turn, max_turn)

    def find_closest_visible(
        self, entities: List, entity_type: type
    ) -> Optional["Entity"]:
        visible_entities = [
            e
            for e in entities
            if isinstance(e, entity_type) 
            and ((hasattr(e, 'available') and e.available) or (hasattr(e, 'alive') and e.alive))
            and self.can_see(e)
        ]

        if not visible_entities:
            return None

        return min(visible_entities, key=self.distance_to)

    def can_see(self, target) -> bool:
        distance = self.distance_to(target)
        vision_range = self.get_vision_range()
        return distance <= vision_range

    def check_reproduction_status(self):
        if self.reproduction_score >= c.REPRODUCTION_SCORE_THRESHOLD:
            self.can_reproduce = True
        else:
            self.can_reproduce = False

    def get_vision_range(self) -> float:
        return (self.genome.vision / 100.0) * 150
