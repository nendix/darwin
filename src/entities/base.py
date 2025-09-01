"""
Base agent class for Darwin simulation.
"""

from dataclasses import dataclass
from typing import Tuple
from ..utils.math_utils import clamp


@dataclass
class BaseAgent:
    """Base class for all simulation agents."""
    x: float = 0.0
    y: float = 0.0
    vx: float = 0.0
    vy: float = 0.0
    energy: float = 100.0
    alive: bool = True
    age: int = 0
    
    # Reproduction-related fields
    food_eaten: int = 0
    kills: int = 0
    reproduction_score: float = 0.0
    has_reproduced: bool = False

    def pos(self) -> Tuple[float, float]:
        """Get agent position as tuple."""
        return (self.x, self.y)

    def tick_energy(self, base_rate: float) -> bool:
        """Consume base energy per tick. Return True if still alive."""
        if not self.alive:
            return False
        self.age += 1
        self.energy -= base_rate
        if self.energy <= 0:
            self.alive = False
            return False
        return True

    def consume_for_move(self, amount: float):
        """Consume energy for movement; may kill the agent if energy hits 0."""
        self.energy = clamp(self.energy - amount, 0.0, self.energy)
        if self.energy <= 0:
            self.alive = False

    def gain_energy(self, amount: float):
        """Gain energy up to maximum stamina from genome."""
        # Max energy is determined by the agent's stamina genome
        # This method should be overridden by subclasses to access their specific genome
        max_energy = getattr(self, '_max_energy', 100.0)  # Fallback
        self.energy = clamp(self.energy + amount, 0.0, max_energy)

    def calculate_reproduction_score(self) -> float:
        """
        Calculate reproduction score based on performance.
        Score = food_eaten * 20 + energy_ratio * 30 + age * 0.1 + kills * 25
        """
        # Energy ratio based on current energy vs max stamina
        max_energy = getattr(self, '_max_energy', 100.0)
        energy_ratio = self.energy / max(1.0, max_energy)
        survival_factor = self.age * 0.1
        food_factor = self.food_eaten * 20
        kill_factor = self.kills * 25
        
        self.reproduction_score = food_factor + energy_ratio * 30 + survival_factor + kill_factor
        return self.reproduction_score

    def can_reproduce(self) -> bool:
        """Check if agent can reproduce (score >= 100 and hasn't reproduced yet)."""
        if self.has_reproduced or not self.alive:
            return False
        
        self.calculate_reproduction_score()
        return self.reproduction_score >= 100.0
