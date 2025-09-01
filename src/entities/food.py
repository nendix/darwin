"""
Food entities for Darwin simulation.
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Food:
    """Basic food entity that provides energy to agents."""
    pos: Tuple[float, float]
