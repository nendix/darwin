"""
DNA and genome definitions for Darwin simulation.
"""

from dataclasses import dataclass


@dataclass
class PreyGenome:
    """Genome for prey entities with survival-focused traits (1-100 range)."""

    speed: float  # 1-100: Movement speed
    vision: float  # 1-100: Detection range
    stamina: float  # 1-100: Maximum energy
    resistance: float  # 1-100: Defense against predators


@dataclass
class PredatorGenome:
    """Genome for predator entities with hunting-focused traits (1-100 range)."""

    speed: float  # 1-100: Movement speed
    vision: float  # 1-100: Detection range
    stamina: float  # 1-100: Maximum energy
    strength: float  # 1-100: Attack power
