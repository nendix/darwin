"""
Prey agent implementation for Darwin simulation.
"""

from dataclasses import dataclass, field
import random
from typing import List, TYPE_CHECKING
from ..utils.math_utils import clamp, dist, normalize
from ..utils.position_utils import clamp_to_bounds, check_collision, resolve_collision
from ..genetics.dna import PreyGenome
from .base import BaseAgent
from .food import Food

if TYPE_CHECKING:
    from .predator import Predator


@dataclass
class Prey(BaseAgent):
    """Prey agent that seeks food and avoids predators."""
    dna: PreyGenome = field(default_factory=lambda: PreyGenome(1, 1, 1, 0))

    def step(self, w: int, h: int, foods: List[Food], predators: List['Predator'], all_prey: List['Prey'], params):
        """Execute one simulation step for this prey."""
        if not self.tick_energy(params.prey_hunger_rate):
            return

        # Convert genome values (1-100) to usable ranges
        actual_speed = self.dna.speed / 100.0 * 3.0 + 0.5  # 0.5-3.5 range
        actual_vision = self.dna.vision / 100.0 * 200.0 + 50.0  # 50-250 range
        max_energy = self.dna.stamina / 100.0 * 200.0 + 50.0  # 50-250 range (stamina = max energy capacity)
        
        # Store max energy for gain_energy method
        self._max_energy = max_energy
        
        # Update reproduction score (for fitness tracking only)
        # Note: age is automatically incremented in tick_energy()
        self.calculate_reproduction_score()

        # Note: Reproduction is abstract - agents don't actually reproduce during simulation
        # The reproduction score is used as fitness measure for evolution between generations

        # detect nearest predator within vision
        nearest_pred = None
        dmin = actual_vision
        for pr in predators:
            if not pr.alive:
                continue
            d = dist(self.pos(), pr.pos())
            if d < dmin:
                dmin = d
                nearest_pred = pr

        # Movement logic: flee predators > seek food > random movement
        ax, ay = 0.0, 0.0
        has_direction = False
        
        if nearest_pred:
            # PRIORITY 1: Flee from predator if in vision
            dx = self.x - nearest_pred.x
            dy = self.y - nearest_pred.y
            nx, ny = normalize(dx, dy)
            ax, ay = nx, ny
            has_direction = True
        else:
            # PRIORITY 2: Seek nearest food within vision
            nearest_food = None
            dminf = actual_vision  # Only see food within vision range
            for f in foods:
                d = dist(self.pos(), f.pos)
                if d < dminf:
                    dminf = d
                    nearest_food = f
                    
            if nearest_food:
                # Move directly toward food
                dx = nearest_food.pos[0] - self.x
                dy = nearest_food.pos[1] - self.y
                nx, ny = normalize(dx, dy)
                ax, ay = nx, ny
                has_direction = True
        
        # PRIORITY 3: Random movement if no food/predator in vision
        if not has_direction:
            # Random direction for exploration
            import math
            angle = random.uniform(0, 2 * math.pi)
            ax = math.cos(angle)
            ay = math.sin(angle)

        # Movement with genome-scaled CONSTANT speed
        # Same speed regardless of activity: fleeing, seeking food, or exploring
        nx, ny = normalize(ax, ay)
        move_cost = params.stamina_drain_move * (0.5 + 0.5 * (actual_speed / 3.5))
        self.consume_for_move(move_cost)
        
        # Apply genome-scaled constant speed movement (always same speed)
        if self.alive:
            self.vx = nx * actual_speed  # Constant speed in direction
            self.vy = ny * actual_speed  # Constant speed in direction
        
        # Apply movement if alive
        if self.alive:
            # Move with constant speed (no velocity accumulation)
            self.x += self.vx
            self.y += self.vy
            
            # Clamp to world bounds (no wrapping)
            self.x, self.y = clamp_to_bounds(self.x, self.y, w, h, radius=5.0)
            
            # Check and resolve collisions with other prey
            for other_prey in all_prey:
                if other_prey != self and other_prey.alive:
                    if check_collision(self.pos(), other_prey.pos(), min_distance=10.0):
                        self.x, self.y = resolve_collision(self.pos(), other_prey.pos(), min_distance=10.0)
                        # Clamp again after collision resolution
                        self.x, self.y = clamp_to_bounds(self.x, self.y, w, h, radius=5.0)
            
            # Note: No collision resolution with predators - collision means attack/death

        # eat food if close (only if alive)
        if self.alive:
            eaten = None
            for i, f in enumerate(foods):
                if dist(self.pos(), f.pos) < 8.0:
                    eaten = i
                    break
            if eaten is not None:
                foods.pop(eaten)
                self.food_eaten += 1
                self.gain_energy(params.prey_food_energy)  # Use stamina-based max energy
