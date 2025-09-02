"""
Predator agent implementation for Darwin simulation.
"""

import random
from dataclasses import dataclass, field
from typing import List, Optional, TYPE_CHECKING
from ..utils.math_utils import clamp, dist, normalize
from ..utils.position_utils import clamp_to_bounds, check_collision, resolve_collision
from ..genetics.dna import PredatorGenome
from .base import BaseAgent

if TYPE_CHECKING:
    from .prey import Prey


@dataclass
class Predator(BaseAgent):
    """Predator agent that hunts prey."""

    dna: PredatorGenome = field(default_factory=lambda: PredatorGenome(1, 1, 1, 1))

    def step(
        self,
        w: int,
        h: int,
        preys: List["Prey"],
        all_predators: List["Predator"],
        params,
    ):
        """Execute one simulation step for this predator."""
        if not self.tick_energy(params.predator_hunger_rate):
            return

        # Convert genome values (1-100) to usable ranges
        actual_speed = self.dna.speed / 100.0 * 3.0 + 0.5  # 0.5-3.5 range
        actual_vision = self.dna.vision / 100.0 * 200.0 + 50.0  # 50-250 range
        max_energy = (
            self.dna.stamina / 100.0 * 200.0 + 50.0
        )  # 50-250 range (stamina = max energy capacity)
        actual_strength = self.dna.strength / 100.0 * 1.3 + 0.2  # 0.2-1.5 range

        # Store max energy for gain_energy method
        self._max_energy = max_energy

        # Update reproduction score (for fitness tracking only)
        # Note: age is automatically incremented in tick_energy()
        self.calculate_reproduction_score()

        # Note: Reproduction is abstract - agents don't actually reproduce during simulation
        # The reproduction score is used as fitness measure for evolution between generations

        # seek nearest prey within vision
        target: Optional["Prey"] = None
        dmin = actual_vision  # Only hunt prey within vision range
        for pr in preys:
            if not pr.alive:
                continue
            d = dist(self.pos(), pr.pos())
            if d < dmin:
                dmin = d
                target = pr

        # Movement logic: hunt visible prey > random exploration
        ax, ay = 0.0, 0.0
        has_direction = False

        if target:
            # PRIORITY 1: Hunt prey within vision
            dx = target.x - self.x
            dy = target.y - self.y
            nx, ny = normalize(dx, dy)
            ax, ay = nx, ny
            has_direction = True

        # PRIORITY 2: Random exploration if no prey in vision
        if not has_direction:
            # Random direction for hunting
            import math

            angle = random.uniform(0, 2 * math.pi)
            ax = math.cos(angle)
            ay = math.sin(angle)

        # Movement with genome-scaled CONSTANT speed
        # Same speed regardless of activity: hunting or exploring
        nx, ny = normalize(ax, ay)
        move_cost = params.stamina_drain_move * 1.2 * (0.5 + 0.5 * (actual_speed / 3.5))
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
            self.x, self.y = clamp_to_bounds(self.x, self.y, w, h, radius=6.0)

            # Check and resolve collisions with other predators
            for other_predator in all_predators:
                if other_predator != self and other_predator.alive:
                    if check_collision(
                        self.pos(), other_predator.pos(), min_distance=12.0
                    ):
                        self.x, self.y = resolve_collision(
                            self.pos(), other_predator.pos(), min_distance=12.0
                        )
                        # Clamp again after collision resolution
                        self.x, self.y = clamp_to_bounds(
                            self.x, self.y, w, h, radius=6.0
                        )

            # Check collisions with prey - collision means automatic attack/kill
            for prey in preys:
                if prey.alive:
                    if check_collision(self.pos(), prey.pos(), min_distance=8.0):
                        # Collision with prey = automatic kill and feeding
                        # Use actual_strength for combat calculation
                        actual_resistance = (
                            prey.dna.resistance / 100.0 * 1.0
                        )  # 0-1 range for resistance
                        advantage = actual_strength - actual_resistance
                        base = 0.35 + max(0.0, advantage) * 0.35
                        base = clamp(base, 0.05, 0.95)
                        if random.random() < base:
                            prey.alive = False
                            self.kills += 1
                            self.gain_energy(params.predator_food_energy)
                        else:
                            # Failed attack - push predator away slightly
                            self.x, self.y = resolve_collision(
                                self.pos(), prey.pos(), min_distance=8.0
                            )
                            self.x, self.y = clamp_to_bounds(
                                self.x, self.y, w, h, radius=6.0
                            )
