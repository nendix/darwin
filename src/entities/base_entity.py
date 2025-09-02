"""
Darwin - Base Entity Class
"""

import math
import pygame
from typing import List, Tuple

from ..config import *


class Entity:
    """Base class for all entities in the simulation"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.alive = True
        
    def update(self, dt: float, entities: List['Entity']):
        """Update entity state"""
        pass
    
    def draw(self, screen: pygame.Surface, camera_offset: Tuple[int, int], show_vision: bool = False):
        """Draw entity on screen"""
        pass
    
    def distance_to(self, other: 'Entity') -> float:
        """Calculate distance to another entity"""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
    
    def angle_to(self, other: 'Entity') -> float:
        """Calculate angle to another entity in radians"""
        return math.atan2(other.y - self.y, other.x - self.x)
