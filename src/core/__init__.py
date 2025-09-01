"""
Core package for Darwin simulation.
"""

from .world import World
from .statistics import Stats, StatisticsCalculator
from .fitness import FitnessCalculator
from .evolution import EvolutionEngine

__all__ = [
    'World', 
    'Stats', 'StatisticsCalculator',
    'FitnessCalculator',
    'EvolutionEngine'
]
